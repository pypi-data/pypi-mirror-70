#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  parser.py
"""
Functions and constants for parsing formulae
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on Pyteomics (https://github.com/levitsky/pyteomics)
#  |  Copyright (c) 2011-2015, Anton Goloborodko & Lev Levitsky
#  |  Licensed under the Apache License, Version 2.0 (the "License");
#  |  you may not use this file except in compliance with the License.
#  |  You may obtain a copy of the License at
#  |
#  |    http://www.apache.org/licenses/LICENSE-2.0
#  |
#  |  Unless required by applicable law or agreed to in writing, software
#  |  distributed under the License is distributed on an "AS IS" BASIS,
#  |  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  |  See the License for the specific language governing permissions and
#  |  limitations under the License.
#  |
#  |  See also:
#  |  Goloborodko, A.A.; Levitsky, L.I.; Ivanov, M.V.; and Gorshkov, M.V. (2013)
#  |  "Pyteomics - a Python Framework for Exploratory Data Analysis and Rapid Software
#  |  Prototyping in Proteomics", Journal of The American Society for Mass Spectrometry,
#  |  24(2), 301–304. DOI: `10.1007/s13361-012-0516-6 <http://dx.doi.org/10.1007/s13361-012-0516-6>`_
#  |
#  |  Levitsky, L.I.; Klein, J.; Ivanov, M.V.; and Gorshkov, M.V. (2018)
#  |  "Pyteomics 4.0: five years of development of a Python proteomics framework",
#  |  Journal of Proteome Research.
#  |  DOI: `10.1021/acs.jproteome.8b00717 <http://dx.doi.org/10.1021/acs.jproteome.8b00717>`_
#
#  Also based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


# stdlib
import re
from collections import defaultdict
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase
from typing import Any, Dict, Iterable, List, Sequence, Union

# this package
from chemistry_tools.elements import ELEMENTS

# this package
import pyparsing  # type: ignore
from ._parser_core import _formula_to_parts, _get_charge, _get_leading_integer, _parse_multiplicity
from .latex import _latex_mapping

_atom = r'([A-Z][a-z+]*)(?:\[(\d+)\])?([+-]?\d+)?'
_atom_re = re.compile(_atom)
_formula_re = re.compile(fr'^({_atom})*$')

relative_atomic_masses = [element.mass for element in ELEMENTS]


# Construct regular expression to match all elements, plus D and T
element_re_dict: Dict[str, List[str]] = {}

for element in (ELEMENTS.symbols + ["D", "T"]):
	if len(element) == 1:
		if element in element_re_dict:
			element_re_dict[element].append("?")
		else:
			element_re_dict[element] = ["?"]
	else:
		upper, lower = list(element)
		if upper in element_re_dict:
			element_re_dict[upper].append(lower)
		else:
			element_re_dict[upper] = [lower]

invalid_uppers = list(ascii_uppercase)
invalid_lowers = {upper: list(ascii_lowercase) for upper in list(ascii_uppercase)}
invalid_re = []

element_re = []
for upper, lowers in element_re_dict.items():
	lowers = sorted(lowers)

	if lowers == ["?"]:
		element_re.append(upper)
		invalid_uppers.remove(upper)
	elif len(lowers) == 1:
		element_re.append(f"{upper}{lowers[0]}")
	elif "?" in lowers:
		lowers.remove("?")
		invalid_uppers.remove(upper)
		for lower in lowers:
			invalid_lowers[upper].remove(lower)
		element_re.append(f"(({upper}[{''.join(lowers)}]?)(?![{''.join(invalid_lowers[upper])}]))(?![a-z])")
		invalid_re.append(f"{upper}[{''.join(lowers)}][{''.join(invalid_lowers[upper])}]+")
		invalid_re.append(f"{upper}[{''.join(invalid_lowers[upper])}]+")
	else:
		invalid_uppers.remove(upper)
		for lower in lowers:
			invalid_lowers[upper].remove(lower)
		element_re.append(f"({upper}[{''.join(lowers)}]?)(?![a-z])")
		invalid_re.append(f"{upper}[{''.join(lowers)}][{''.join(invalid_lowers[upper])}]+")
		invalid_re.append(f"{upper}[{''.join(invalid_lowers[upper])}]+")

# print(invalid_uppers, invalid_lowers)

element_re.sort()

# Isotopes either as [C12], C[12] or [12C]
isotopes_re = []
for elem in element_re:
	isotopes_re.append(rf"\b{elem}\[[0-9]+\]")
	isotopes_re.append(rf"\[{elem}[0-9]+\]")
	isotopes_re.append(rf"\[[0-9]+{elem}\]")


@lru_cache()
def _get_formula_parser():
	"""
	Create a forward pyparsing parser for chemical formulae

	BNF for simple chemical formula (no nesting)

		integer :: '0'..'9'+
		element :: 'A'..'Z' 'a'..'z'*
		term :: element [integer]
		formula :: term+


	BNF for nested chemical formula

		integer :: '0'..'9'+
		element :: 'A'..'Z' 'a'..'z'*
		term :: (element | '(' formula ')') [integer]
		formula :: term+

	Notes
	-----
	Based on http://stackoverflow.com/a/18555142/790973
	Copyright 2013 Paul McGuire (http://stackoverflow.com/users/165216/paul-mcguire)
	Licensed under CC-BY-SA 3.0.
	"""

	Forward, Group, OneOrMore = pyparsing.Forward, pyparsing.Group, pyparsing.OneOrMore
	Optional, ParseResults = pyparsing.Optional, pyparsing.ParseResults
	Suppress, Word, nums = pyparsing.Suppress, pyparsing.Word, pyparsing.nums

	LPAR, RPAR = map(Suppress, "()")
	integer = Word(nums)

	# add parse action to convert integers to ints, to support doing addition
	# and multiplication at parse time
	integer.setParseAction(lambda t: int(t[0]))

	element = pyparsing.Regex('|'.join(isotopes_re + element_re) + "$")

	# element = pyparsing.Regex(
	# 		r"A[cglmrstu]|B[aehikr]?|C[adeflmorsu]?|D[bsy]|E[rsu]|F[emr]?|G[ade]"
	# 		r"|H[efgos]?|I[nr]?|Kr?|L[airu]|M[dgnot]|N[abdeiop]?|Os?|P[abdmortu]?"
	# 		r"|R[abefghnu]|S[bcegimnr]?|T[abcehilm]|Uu[bhopqst]|U|V|W|Xe|Yb?|Z[nr]")

	# forward declare 'formula' so it can be used in definition of 'term'
	formula = Forward()

	term = Group(
			(element | Group(LPAR + formula + RPAR)("subgroup"))
			+ Optional(integer, default=1)("mult")
			)

	# add parse actions for parse-time processing

	# parse action to multiply out subgroups
	def multiplyContents(tokens):
		t = tokens[0]
		# if these tokens contain a subgroup, then use multiplier to
		# extend counts of all elements in the subgroup
		if t.subgroup:
			mult = t.mult
			for term in t.subgroup:
				term[1] *= mult
			return t.subgroup

	term.setParseAction(multiplyContents)

	# add parse action to sum up multiple references to the same element
	def sum_by_element(tokens):
		elementsList = [t[0] for t in tokens]

		# construct set to see if there are duplicates
		duplicates = len(elementsList) > len(set(elementsList))

		# if there are duplicate element names, sum up by element and
		# return a new nested ParseResults
		if duplicates:
			ctr = defaultdict(int)
			for t in tokens:
				ctr[t[0]] += t[1]
			return ParseResults([ParseResults([k, v]) for k, v in ctr.items()])

	# define contents of a formula as one or more terms
	formula << OneOrMore(term)
	formula.setParseAction(sum_by_element)

	return formula


def _parse_stoich(stoich) -> Dict[int, Any]:
	if stoich == 'e':  # special case, the electron is not an element
		return {}

	symbols = ELEMENTS.symbols + ["D", "T"]

	if re.findall('|'.join(invalid_re), stoich):
		raise ValueError(f"Unrecognised formula: {stoich}")

	return {
			symbols.index(k) + 1: n for k, n
			in _get_formula_parser().parseString(stoich)
			}


def string_to_composition(
		formula: str, prefixes: Iterable[str] = None,
		suffixes: Sequence[str] = ('(s)', '(l)', '(g)', '(aq)'),
		) -> Dict[int, int]:
	"""
	Parse composition of formula representing a chemical formula

	**Examples**
	>>> string_to_composition('NH4+') == {0: 1, "H": 4, "N": 1}
	True
	>>> string_to_composition('.NHO-(aq)') == {0: -1, "H": 1, "N": 1, "O": 1}
	True
	>>> string_to_composition('Na2CO3.7H2O') == {"Na": 2, "C": 1, "O": 10, "H": 14}
	True

	:param formula: Chemical formula, e.g. 'H2O', 'Fe+3', 'Cl-'
	:type formula: str
	:param prefixes: Prefixes to ignore, e.g. ('.', 'alpha-')
	:param suffixes: Suffixes to ignore, e.g. ('(g)', '(s)')

	:return: The composition, as a dictionary mapping atomic number -> multiplicity.
		"Atomic number" 0 represents net charge.
	"""

	if prefixes is None:
		prefixes = _latex_mapping.keys()

	stoich_tok, chg_tok = _formula_to_parts(formula, prefixes, suffixes)[:2]
	tot_comp = {}
	parts = stoich_tok.split('.')

	for idx, stoich in enumerate(parts):
		if idx == 0:
			m = 1
		else:
			m, stoich = _get_leading_integer(stoich)

		# comp = _parse_stoich(stoich)
		if stoich == 'e':  # special case, the electron is not an element
			comp = {}
		else:
			try:
				if re.findall('|'.join(invalid_re), stoich):
					raise ValueError(f"Unrecognised formula: {formula}")

				comp = _get_formula_parser().parseString(stoich)
			except pyparsing.ParseException:
				raise ValueError(f"Unrecognised formula: {formula}")

		# for k, v in comp.items():
		for k, v in comp:
			if k not in tot_comp:
				tot_comp[k] = m * v
			else:
				tot_comp[k] += m * v

	if chg_tok is not None:
		tot_comp[0] = _get_charge(chg_tok)

	return tot_comp

#
# def to_reaction(line, substance_keys, token, cls, globals_=None, **kwargs):
# 	"""
# 	Parses a string into a Reaction object and substances
#
# 	Reac1 + 2 Reac2 + (2 Reac1) -> Prod1 + Prod2; 10**3.7; ref='doi:12/ab'
# 	Reac1 = Prod1; 2.1;
#
# 	Parameters
# 	----------
# 	line: str
# 		string representation to be parsed
# 	substance_keys: iterable of strings
# 		Allowed names, e.g. ('H2O', 'H+', 'OH-')
# 	token : str
# 		delimiter token between reactant and product side
# 	cls : class
# 		e.g. subclass of Reaction
# 	globals_: dict (optional)
# 		Globals passed on to :func:`eval`, when ``None``:
# 		`chempy.units` is used with 'chempy'
# 		and 'default_units' extra entries.
#
# 	Notes
# 	-----
# 	This function calls :func:`eval`, hence there are severe security concerns
# 	with running this on untrusted data.
#
# 	"""
#
# 	parts = line.rstrip('\n').split(';')
# 	stoich = parts[0].strip()
# 	if len(parts) > 2:
# 		kwargs.update(eval('dict(' + ';'.join(parts[2:]) + '\n)', globals_ or {}))
# 	if len(parts) > 1:
# 		param = parts[1].strip()
# 	else:
# 		param = kwargs.pop('param', 'None')
#
# 	if isinstance(param, str):
# 		param = None if globals_ is False else eval(param, globals_)
#
# 	if token not in stoich:
# 		raise ValueError("Missing token: %s" % token)
#
# 	reac_prod = [[y.strip() for y in x.split(' + ')] for x in stoich.split(token)]
#
# 	act, inact = [], []
# 	for elements in reac_prod:
# 		act.append(_parse_multiplicity([x for x in elements if not x.startswith('(')], substance_keys))
# 		inact.append(_parse_multiplicity(
# 				[x[1:-1] for x in elements if x.startswith('(') and x.endswith(')')],
# 				substance_keys
# 				))
#
# 	# stoich coeff -> dict
# 	return cls(act[0], act[1], param, inact_reac=inact[0], inact_prod=inact[1], **kwargs)


def mass_from_composition(composition: Dict[Union[str, int], int], charge: int = 0) -> float:
	"""
	Calculates molecular mass from atomic weights.

	.. note::

		Atomic number 0 denotes charge or "net electron defficiency"


	:param composition: Dictionary mapping str or int (element symbol or atomic number) to int (coefficient)
	:param charge: The charge of the composition.
	:type charge: int

	:return: Molecular weight in atomic mass units
	:rtype: float

	**Example**

	>>> f'{mass_from_composition({0: -1, "H": 1, 8: 1}):.2f}'
	'17.01'
	"""

	if charge and 0 in composition:
		if charge != composition[0]:
			raise ValueError(
					"'charge' can only be specified once, "
					"either as a keyword argument or as the '0' key of 'composition'")

	mass = 0.0

	for k, v in composition.items():
		if k == 0:  # electron
			mass -= v * 5.489e-4
		elif isinstance(k, str):
			mass += v * ELEMENTS[k].mass
		elif isinstance(k, int):
			mass += v * ELEMENTS[k].mass

	return mass

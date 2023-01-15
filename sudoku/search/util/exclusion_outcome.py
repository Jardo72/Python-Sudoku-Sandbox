#
# Copyright 2023 Jaroslav Chmurny
#
# This file is part of Python Sudoku Sandbox V2.
#
# Python Sudoku Sandbox is free software developed for educational and
# experimental purposes. It is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from enum import unique, Enum


@unique
class ExclusionOutcome(Enum):
    """
    Defines possible outcomes of an exclusion, for instance an exclusion of a candidate
    value for a single undefined cell. The meaning of particular enum elements is the
    following:
    * UNAMBIGUOUS_CANDIDATE_FOUND indicates that after the exclusion of a candidate, there
      is only single applicable candidate remaining. This outcome inidcates that an
      unambiguous candidate has been found by the exclusion.
    * UNAMBIGUOUS_CANDIDATE_NOT_FOUND indicates that the exclusion has not identified an
      unambiguous candidate. This value is to be used in several situations, for instance
      if two or more applicable candidates are still remaining after the exclusion, or if
      the exclusion of a candidate has not changed the set of candidates as the candidate
      was already excluded.
    This enum is internal, there is no need to use it directly in other modules.
    """

    UNAMBIGUOUS_CANDIDATE_FOUND = 1

    UNAMBIGUOUS_CANDIDATE_NOT_FOUND = 2
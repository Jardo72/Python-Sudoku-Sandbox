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

from dataclasses import dataclass

from sudoku.grid import CellAddress
from .candidate_list import CandidateList


@dataclass(frozen=True, slots=True)
class UnambiguousCandidate:
    """
    Immutable structure carrying information about an unambiguous candidate for an
    undefined cell. Besides the only applicable candidate value, this structure also
    carries the address (i.e. the row and the column) of the concerned cell.
    """
    cell_address: CellAddress
    value: int

    def as_candidate_list(self) -> CandidateList:
        """
        Creates and returns a new candidate list representing this unambiguous candidate.
        The returned candidate list has the same cell address as this unambiguous candidate,
        and it carries a single candidate value, namely the value of this unambiguous candidate.
        """
        return CandidateList(self.cell_address, (self.value, ))

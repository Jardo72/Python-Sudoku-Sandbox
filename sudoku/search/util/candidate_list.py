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
from typing import Sized, Tuple

from sudoku.grid import CellAddress


@dataclass(frozen=True, slots=True)
class CandidateList(Sized):
    """
    Immutable structure carrying all candidate values applicable to a single undefined
    cell. Besides the applicable candidate values, this structure also carries the
    address (i.e. the row and the column) of the concerned cell.
    """
    cell_address: CellAddress
    values: Tuple[int, ...]

    def __len__(self) -> int:
        return len(self.values)

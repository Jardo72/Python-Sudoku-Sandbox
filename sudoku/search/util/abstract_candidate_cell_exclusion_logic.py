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

from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from typing import List, Optional

from sudoku.grid import CellAddress
from .unambiguous_candidate import UnambiguousCandidate


class AbstractCandidateCellExclusionLogic(ABC):
    """
    Abstract base class prescribing the interface the cell exclusion logic implementations have
    to implement.
    """

    @abstractmethod
    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> Optional[List[UnambiguousCandidate]]:
        """
        Applies the given cell value to the cell with the given coordinates and excludes
        all peers of the given cell as candidate cells for the given value.

        Args:
            cell_address (CellAddress):     The coordinates of the cell the given value is to
                                            be applied to.
            value (int):                    The value for the given cell.

        Returns:
            List of UnambiguousCandidate instances, one for each of those cells which have
            been identified as unambiguous candidate cells with any region for any value.
            None is returned if the exclusion has not led to any cell being identified as
            unambiguous candidate cell.
        """
        ...

    @abstractmethod
    def copy(self) -> AbstractCandidateCellExclusionLogic:
        """
        Creates and returns a copy of this object which behaves as if it was a deep copy
        of this object.
        """
        ...

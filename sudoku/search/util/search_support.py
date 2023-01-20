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
from collections import deque
from logging import getLogger
from typing import Deque, Optional

from sudoku.grid import CellAddress, CellStatus, Grid
from sudoku.grid import get_all_cell_addresses
from .abstract_candidate_cell_exclusion_logic import AbstractCandidateCellExclusionLogic
from .candidate_list import CandidateList
from .candidate_query_mode import CandidateQueryMode
from .candidate_value_exclusion_logic import CandidateValueExclusionLogic
from .null_cell_exclusion_logic import NullCandidateCellExclusionLogic
from .unambiguous_candidate import UnambiguousCandidate


_logger = getLogger(__name__)


class SearchSupport:
    """
    Helper class supporting implementation of search algorithms. An instance of
    this class aggregates and coordinates a grid with a candidate value exclusion
    logic keeping track of applicable candidate values for the grid.
    """

    def __init__(self, grid: Optional[Grid] = None, original: Optional[SearchSupport] = None) -> None:
        if self._is_ordinary_constructor(grid, original):
            self._init_from_scratch(grid)  # type: ignore
        elif self._is_copy_constructor(grid, original):
            self._init_from_other_instance(original)  # type: ignore
        else:
            message = "Invalid arguments. Exactly one of the two arguments is expected."
            raise ValueError(message)

    @staticmethod
    def _is_ordinary_constructor(grid: Optional[Grid], original: Optional[SearchSupport]) -> bool:
        return original is None and isinstance(grid, Grid)

    @staticmethod
    def _is_copy_constructor(grid: Optional[Grid], original: Optional[SearchSupport]) -> bool:
        return grid is None and isinstance(original, SearchSupport)

    def _create_candidate_cell_exclusion_logic(self) -> AbstractCandidateCellExclusionLogic:
        return NullCandidateCellExclusionLogic()

    def _init_from_scratch(self, grid: Grid) -> None:
        self._value_exclusion_logic = CandidateValueExclusionLogic()
        self._cell_exclusion_logic = self._create_candidate_cell_exclusion_logic()
        self._candidate_queue: Deque = deque()
        self._grid = grid
        for cell_address in get_all_cell_addresses():
            if grid.get_cell_status(cell_address) is CellStatus.PREDEFINED:
                value = grid.get_cell_value(cell_address)
                candidate_list = self._value_exclusion_logic.apply_and_exclude_cell_value(cell_address, value)  # type: ignore
                if candidate_list is not None:
                    self._candidate_queue.extend(candidate_list)
                candidate_list = self._cell_exclusion_logic.apply_and_exclude_cell_value(cell_address, value)  # type: ignore
                if candidate_list is not None:
                    self._candidate_queue.extend(candidate_list)

    def _init_from_other_instance(self, original: SearchSupport) -> None:
        self._value_exclusion_logic = original._value_exclusion_logic.copy()
        self._cell_exclusion_logic = original._cell_exclusion_logic.copy()
        self._candidate_queue = original._candidate_queue.copy()
        self._grid = original._grid.copy()

    def get_grid_snapshot(self) -> Grid:
        """
        Creates and returns a clone of the underlying grid. Modification of the returned snapshot
        will not impact the internal state of this object.
        """
        return self._grid.copy()

    def set_cell_value(self, cell_address: CellAddress, value: int) -> None:
        """
        Sets the cell with the given coordinates to the given value, assumed the
        cell with the given coordinates is empty (i.e. its value is undefined).
        Subsequently, excludes the given value from applicable candidate values
        for the peers of the given cell. If the exclusion identifies unambiguous
        candidate(s) for any undefined cell(s), the unambiguous candidates are
        retained so that they can be provided by the get_unambiguous_candidate
        method.

            Parameters:
                cell_address (CellAddress):    The coordinates of the cell whose value
                                               is to be set.
                value (int):                   The new value for the given cell.

            Raises:
                ValueError      If the given cell has already a value, regardless
                                of whether the value was defined in the original
                                puzzle or completed during the search.
        """
        self._grid.set_cell_value(cell_address, value)
        candidate_list = self._value_exclusion_logic.apply_and_exclude_cell_value(cell_address, value)
        _logger.info("Assignment %s = %d completed, outcome of value exclusion is %s", cell_address, value, candidate_list)
        if candidate_list is not None:
            self._candidate_queue.extend(candidate_list)
        candidate_list = self._cell_exclusion_logic.apply_and_exclude_cell_value(cell_address, value)
        _logger.info("Assignment %s = %d completed, outcome of cell exclusion is %s", cell_address, value, candidate_list)
        if candidate_list is not None:
            self._candidate_queue.extend(candidate_list)

    def has_completed_grid(self) -> bool:
        """
        Verifies whether the underlying grid is already completed.

        Returns:
            bool: True if and only if none of the cells of the underlying grid is empty; False if
                  the underlying grid contains at least one empty cell.
        """
        return self._grid.is_complete()

    def has_empty_cells_without_applicable_candidates(self) -> bool:
        """
        Verifies whether the underlying grid contains at least one undefined cell for
        which all nine values have been already excluded (i.e. no candidate value is
        applicable to the cell).

            Returns:
                bool: True if and only if the underlying grid contains at least one undefined cell
                      for which all nine values have been already excluded. False if at least one
                      candidate value is applicable to each undefined cell of underlying grid.
        """
        for cell_address in get_all_cell_addresses():
            cell_status = self._grid.get_cell_status(cell_address)
            if cell_status is not CellStatus.UNDEFINED:
                continue
            if self._value_exclusion_logic.get_applicable_value_count(cell_address) == 0:
                _logger.info("Cell %s undefined, but there are no applicable candidates", cell_address)
                return True
        return False

    def get_unambiguous_candidate(self) -> Optional[UnambiguousCandidate]:
        """
        Returns the next unambiguous candidate identified by one of the former
        invocations of the set_cell_value method. None is returned if there is
        no unambiguous candidate.
        """
        while len(self._candidate_queue) > 0:
            candidate = self._candidate_queue.popleft()
            _logger.debug("Candidate taken from queue: %s", candidate)
            if self._value_exclusion_logic.is_applicable(candidate):
                _logger.debug("Candidate still applicable, going to return it")
                return candidate
            else:
                _logger.debug("Candidate not applicable anymore, cannot return it")
        return None

    def get_undefined_cell_candidates(self, mode: CandidateQueryMode) -> Optional[CandidateList]:
        """
        Returns candidate values applicable to one of the undefined cells of the
        underlying grid.
        Args:
            mode:    One of the elements of the CandidateQueryMode enum determining
                     which of the undefined cells of the underlying grid is to be
                     taken into account.
        """
        result = self._value_exclusion_logic.get_undefined_cell_candidates(mode)
        if result:
            _logger.info("Undefined cell candidates found (mode = %s): %s", mode, result)
            assert self._grid.get_cell_status(result.cell_address) is CellStatus.UNDEFINED
        else:
            _logger.debug("No undefined cell candidates, returning None")
        return result

    def copy(self) -> SearchSupport:
        """
        Creates and returns a copy of this object which behaves as if it was a deep copy
        of this object.

        Returns:
            SearchSupport: The created clone of this object. Be aware of the fact that
                           the returned object is semantically equivalent to deep copy
                           of this object. In other words, any modification of the clone will
                           not change the status of this object and vice versa.
        """
        return SearchSupport(original=self)


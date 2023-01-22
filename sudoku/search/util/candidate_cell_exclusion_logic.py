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
from logging import getLogger
from typing import List, Optional, Tuple

from sudoku.grid import CellAddress
from sudoku.grid import get_cell_address
from .abstract_candidate_cell_exclusion_logic import AbstractCandidateCellExclusionLogic
from .exclusion_outcome import ExclusionOutcome
from .unambiguous_candidate import UnambiguousCandidate


_logger = getLogger(__name__)


class _RegionCandidateCells:
    """
    Internal helper class that keeps track of cells within a region where a particular
    value is applicable.
    """

    _row_peers = {0: 0b111111000, 1: 0b111000111, 2: 0b000111111}

    _column_peers = {0: 0b110110110, 1: 0b101101101, 2: 0b011011011}

    def __init__(
        self, topmost_row: int, leftmost_column: int, value: int, bitmask: int = 0b111111111,
        applicable_cell_count: int = 9
    ) -> None:
        self._topmost_row = topmost_row
        self._leftmost_column = leftmost_column
        self._value = value
        self._bitmask = bitmask
        self._applicable_cell_count = applicable_cell_count

    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> ExclusionOutcome:
        _logger.debug("Going to apply/exclude value %d for %s", value, cell_address)
        row_within_region, column_within_region = self._get_cell_coordinates_within_this_region(cell_address)
        _logger.debug("Cell address within region [%d, %d]", row_within_region, column_within_region)
        if (row_within_region, column_within_region) == (-1, -1):
            # cell not contained in this region, and neither the row, nor the column
            # containing the cell is crossing this region => nothing to be excluded
            _logger.debug("Ignoring region starting at [%d, %d] for the value %d", self._topmost_row, self._leftmost_column, self._value)
            return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        if row_within_region in [0, 1, 2] and column_within_region not in [0, 1, 2]:
            _logger.debug("Row is crossing this region")
            # cell not contained in this region, but the row containing the cell is
            # crossing this region; depending on the value, we have to exclude either
            # nothing, or all peers of the cell
            if value != self._value:
                _logger.debug("Ignoring the value %d (my value is %d)", value, self._value)
                return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
            peers_mask = _RegionCandidateCells._row_peers[row_within_region]
            _logger.debug("Peers mask (row) = %s, current status = %s", format(peers_mask, 'b'), format(self._bitmask, 'b'))
            self._bitmask = self._bitmask & peers_mask
            _logger.debug("New status = %s", format(self._bitmask, 'b'))
            return self._update_applicable_value_count()

        if column_within_region in [0, 1, 2] and row_within_region not in [0, 1, 2]:
            _logger.debug("Column is crossing this region")
            # cell not contained in this region, but the column containing the cell is
            # crossing this region; depending on the value, we have to exclude either
            # nothing, or all peers of the cell
            if value != self._value:
                _logger.debug("Ignoring the value %d (my value is %d)", value, self._value)
                return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
            peers_mask = _RegionCandidateCells._column_peers[column_within_region]
            _logger.debug("Peers mask (column) = %s, current status = %s", format(peers_mask, 'b'), format(self._bitmask, 'b'))
            self._bitmask = self._bitmask & peers_mask
            _logger.debug("New status = %s", format(self._bitmask, 'b'))
            return self._update_applicable_value_count()

        # cell contained in this region; depending on the value, we have to exclude either
        # a single cell, or the entire region
        if self._value == value:
            _logger.debug("Excluding complete region")
            self._bitmask = 0
            self._applicable_cell_count = 0
            return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        _logger.debug("Excluding single cell")
        cell_mask = 1 << (3 * row_within_region + column_within_region)
        cell_mask = 0b111111111 ^ cell_mask
        self._bitmask = self._bitmask & cell_mask
        _logger.debug("New status = %s", format(self._bitmask, 'b'))
        return self._update_applicable_value_count()

    def _get_cell_coordinates_within_this_region(self, cell_address: CellAddress) -> Tuple[int, int]:
        row, column = cell_address.row, cell_address.column
        row_within_region, column_within_region = (-1, -1)
        if (3 * (row // 3)) == self._topmost_row:
            row_within_region = row - self._topmost_row
        if (3 * (column // 3)) == self._leftmost_column:
            column_within_region = column - self._leftmost_column

        return (row_within_region, column_within_region)

    def _update_applicable_value_count(self) -> ExclusionOutcome:
        new_count = 0
        for shift in range(0, 9):
            mask = 1 << shift
            if self._bitmask & mask == mask:
                new_count += 1

        _logger.debug("Going to update the value count from %d to %d", self._applicable_cell_count, new_count)
        result = ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
        if new_count == 1 and self._applicable_cell_count > new_count:
            result = ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND
        self._applicable_cell_count = new_count
        return result

    def get_single_remaining_applicable_cell(self) -> Optional[UnambiguousCandidate]:
        assert self._applicable_cell_count == 1, \
            f"Cannot provide single remaining applicable cell ({self._applicable_cell_count} candidates remaining)."
        _logger.debug("Remaining bitmask = %s", format(self._bitmask, 'b'))
        for i in range(0, 9):
            mask = 1 << i
            if self._bitmask & mask == mask:
                row = self._topmost_row + (i // 3)
                column = self._leftmost_column + (i % 3)
                result = UnambiguousCandidate(get_cell_address(row, column), self._value)
                _logger.debug("%s will be returned", result)
                return result
        _logger.debug("None will be returned")
        return None

    def copy(self) -> _RegionCandidateCells:
        """
        Creates and returns a deep copy of this object.
        """
        return _RegionCandidateCells(self._topmost_row, self._leftmost_column, self._value, self._bitmask, self._applicable_cell_count)


class _RegionGrid:
    """
    Internal helper class supporting candidate cell exclusion. Single instance of this class
    aggregates 9 instances of _RegionCandidateCells.
    """

    def __init__(self, value: Optional[int], regions: Optional[Tuple[_RegionCandidateCells, ...]] = None) -> None:
        if value is not None and regions is None:
            self._regions = tuple([_RegionCandidateCells(row, column, value) for row in [0, 3, 6] for column in [0, 3, 6]])  # type: ignore
        elif value is None and regions is not None:
            self._regions = regions
        else:
            # TODO: invalid arguments
            ...

    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> List[UnambiguousCandidate]:
        result = None
        for region in self._regions:
            exclusion_outcome = region.apply_and_exclude_cell_value(cell_address, value)
            if exclusion_outcome is ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND:
                result = result if result is not None else []
                candidate = region.get_single_remaining_applicable_cell()
                if candidate:
                    result.append(candidate)
        return result

    def copy(self) -> _RegionGrid:
        """
        Creates and returns a deep copy of this object.
        """
        regions_copy = tuple([single_region.copy() for single_region in self._regions])
        return _RegionGrid(None, regions_copy)


class CandidateCellExclusionLogic(AbstractCandidateCellExclusionLogic):
    """
    Logic responsible for exclusion of candidate cells where a particular value is
    not applicable. The exclusion leads to identification of the only cell within
    a region where a value is applicable (other cells within the region have been
    excluded for the value). For such a cell, the value is considered as unambiguous
    candidate value. This class is an internal helper that should not be used directly
    by other packages.
    """

    def __init__(self, original_exclusion_logic: Optional[CandidateCellExclusionLogic] = None) -> None:
        if original_exclusion_logic is None:
            self._region_grids: Tuple[_RegionGrid, ...] = tuple([_RegionGrid(value) for value in range(1, 10)])
        else:
            self._region_grids = tuple([grid.copy() for grid in original_exclusion_logic._region_grids])

    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> Optional[List[UnambiguousCandidate]]:
        """
        Applies the given cell value to the cell with the given coordinates and excludes
        all peers of the given cell as candidate cells for the given value.

            Parameters:
                cell_address (CellAddress):     The coordinates of the cell the given value is to
                                                be applied to.
                value (int):                    The value for the given cell.

            Returns:
                List of UnambiguousCandidate instances, one for each of those cells which have
                been identified as unambiguous candidate cells with any region for any value.
                None is returned if the exclusion has not led to any cell being identified as
                unambiguous candidate cell.
        """
        _logger.debug("Going to apply & exclude the value %d for the cell %s", value, cell_address)
        result = None
        for grid in self._region_grids:
            partial_result = grid.apply_and_exclude_cell_value(cell_address, value)
            if partial_result is not None:
                result = result if result is not None else []
                result += partial_result
        return result

    def copy(self) -> CandidateCellExclusionLogic:
        """
        Creates and returns a copy of this object which behaves as if it was a deep copy
        of this object.

            Returns:
                CandidateCellExclusionLogic: The created clone of this object. Be aware of the fact that
                                             the returned object is semantically equivalent to deep copy
                                             of this object. In other words, any modification of the clone will
                                             not change the status of this object and vice versa.
        """
        return CandidateCellExclusionLogic(self)

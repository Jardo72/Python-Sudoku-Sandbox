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

from logging import getLogger


_logger = getLogger(__name__)


class _RegionCandidateCells:
    """
    Keeps track of cells within a region where a particular value is applicable.
    """

    __row_peers = {0: 0b111111000, 1: 0b111000111, 2: 0b000111111}

    __column_peers = {0: 0b110110110, 1: 0b101101101, 2: 0b011011011}

    def __init__(self, topmost_row: int, leftmost_column: int, value: int, bitmask: int = 0b111111111, applicable_cell_count: int = 9) -> None:
        self._topmost_row = topmost_row
        self._leftmost_column = leftmost_column
        self._value = value
        self._bitmask = bitmask
        self._applicable_cell_count = applicable_cell_count

    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> :
        _logger.debug("Going to apply/exclude value %d for [%d, %d]", value, row, column)
        row_within_region, column_within_region = self.__get_cell_coordinates_within_this_region(row, column)
        _logger.debug("Cell address within region [%d, %d]", row_within_region, column_within_region)
        if (row_within_region, column_within_region) == (-1, -1):
            # cell not contained in this region, and neither the row, nor the column
            # containing the cell is crossing this region => nothing to be excluded
            _logger.debug("Ignoring region starting at [%d, %d] for the value %d", self._topmost_row, self._leftmost_column, self._value)
            return _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        if row_within_region in [0, 1, 2] and column_within_region not in [0, 1, 2]:
            _logger.debug("Row is crossing this region")
            # cell not contained in this region, but the row containing the cell is
            # crossing this region; depending on the value, we have to exclude either
            # nothing, or all peers of the cell
            if value != self._value:
                _logger.debug("Ignoring the value %d (my value is %d)", value, self._value)
                return _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
            peers_mask = _RegionCandidateCells.__row_peers[row_within_region]
            _logger.debug("Peers mask (row) = %s, current status = %s", format(peers_mask, 'b'), format(self._bitmask, 'b'))
            self._bitmask = self._bitmask & peers_mask
            _logger.debug("New status = %s", format(self._bitmask, 'b'))
            return self.__update_applicable_value_count()

        if column_within_region in [0, 1, 2] and row_within_region not in [0, 1, 2]:
            _logger.debug("Column is crossing this region")
            # cell not contained in this region, but the column containing the cell is
            # crossing this region; depending on the value, we have to exclude either
            # nothing, or all peers of the cell
            if value != self._value:
                _logger.debug("Ignoring the value %d (my value is %d)", value, self._value)
                return _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
            peers_mask = _RegionCandidateCells.__column_peers[column_within_region]
            _logger.debug("Peers mask (column) = %s, current status = %s", format(peers_mask, 'b'), format(self._bitmask, 'b'))
            self._bitmask = self._bitmask & peers_mask
            _logger.debug("New status = %s", format(self._bitmask, 'b'))
            return self.__update_applicable_value_count()

        # cell contained in this region; depending on the value, we have to exclude eihter
        # a single cell, or the entire region
        if self._value == value:
            _logger.debug("Excluding complete region")
            self._bitmask = 0
            self._applicable_cell_count = 0
            return _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        _logger.debug("Excluding single cell")
        cell_mask = 1 << (3 * row_within_region + column_within_region)
        cell_mask = 0b111111111 ^ cell_mask
        self._bitmask = self._bitmask & cell_mask
        _logger.debug("New status = %s", format(self._bitmask, 'b'))
        return self.__update_applicable_value_count()


    def __get_cell_coordinates_within_this_region(self, row, column):
        row_within_region, column_within_region = (-1, -1)
        if (3 * (row // 3)) == self._topmost_row:
            row_within_region = row - self._topmost_row
        if (3 * (column // 3)) == self._leftmost_column:
            column_within_region = column - self._leftmost_column

        return (row_within_region, column_within_region)


    def __update_applicable_value_count(self):
        new_count = 0
        for shift in range(0, 9):
            mask = 1 << shift
            if self._bitmask & mask == mask:
                new_count += 1
        
        _logger.debug("Going to update the value count from %d to %d", self._applicable_cell_count, new_count)
        result = _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND
        if new_count == 1 and self._applicable_cell_count > new_count:
            result = _ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND
        self._applicable_cell_count = new_count
        return result


    def get_single_remaining_applicable_cell(self):
        if self._applicable_cell_count != 1:
            message = "Cannot provide single remaining applicable cell ({0} candidates remaining)."
            raise RuntimeError(message.format(self._applicable_value_count))
        _logger.debug("Remaining bitmask = %s", format(self._bitmask, 'b'))
        for i in range(0, 9):
            mask = 1 << i
            if self._bitmask & mask == mask:
                row = self._topmost_row + (i // 3)
                column = self._leftmost_column + (i % 3)
                result = UnambiguousCandidate(row, column, self._value)
                _logger.debug("%s will be returned", result)
                return result
        _logger.debug("None will be returned")


    def copy(self):
        """
        Creates and returns a deep copy of this object.
        """
        return _RegionCandidateCells(self._topmost_row, self._leftmost_column, self._value, self._bitmask, self._applicable_cell_count)

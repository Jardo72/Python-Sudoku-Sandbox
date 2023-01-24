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
from sudoku.grid import get_all_cell_addresses, get_peer_addresses
from .exclusion_outcome import ExclusionOutcome
from .candidate_list import CandidateList
from .candidate_query_mode import CandidateQueryMode
from .unambiguous_candidate import UnambiguousCandidate


_logger = getLogger(__name__)


class _CandidateValues:
    """
    Internal helper that keeps track of applicable candidate values for a single cell. An
    instance of this class is to be updated whenever one of the peers of the cell corresponding
    to the instance of this class is updated. For better understanding, let's assume the
    following example. An instance of this class corresponds to an undefined cell. The row
    containing the cell contains another undefined cells, and the value of one of them is set
    to 5. The above mentioned instance of this class has to be updated via the exclude_value
    method as the value 5 is not applicable anymore.
    """

    def __init__(self, bitmask: int = 0b111111111, applicable_value_count: int = 9) -> None:
        self._bitmask = bitmask
        self._applicable_value_count = applicable_value_count

    def clear(self) -> None:
        """
        Eliminates all candidate values for the cell corresponding to this object. After an
        invocation of this method, no value is applicable to the cell corresponding to this
        object.
        """
        self._bitmask = 0
        self._applicable_value_count = 0

    @property
    def applicable_value_count(self) -> int:
        """
        Number of candidate values applicable to the cell corresponding to this object.
        """
        return self._applicable_value_count

    @property
    def applicable_values(self) -> Tuple[int, ...]:
        """
        Immutable collection with candidate values applicable to the cell corresponding to this object.
        """
        result = [value for value in range(1, 10) if self._bitmask & (1 << (value - 1))]
        return tuple(result)

    def exclude_value(self, value: int) -> ExclusionOutcome:
        """
        Excludes the given value from the applicable candidate values for the cell corresponding to
        this object.

        Args:
            value (int):    The value to be excluded.

        Returns:
            ExclusionOutcome:      Enum value indicating whether the exclusion has led to identification
                                   of an unambiguous candidate value for the cell corresponding to this
                                   object.
        """
        _logger.debug("Going to exclude the value %d, bitmask before exclusion = %s", value, format(self._bitmask, "b"))
        value_mask = 1 << (value - 1)
        if self._bitmask & value_mask == value_mask:
            self._bitmask ^= value_mask
            _logger.debug("Bitmask after exclusion = %s", format(self._bitmask, "b"))
            self._applicable_value_count -= 1
            if self._applicable_value_count == 1:
                return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND
        return ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

    def get_single_remaining_applicable_value(self) -> int:  # type: ignore
        """
        Returns the one and only candidate value applicable to the cell corresponding to this object.
        This method can only be invoked if there is only one applicable candidate value. Otherwise,
        an invocation of this method will fail.
        """
        assert self._applicable_value_count == 1, \
            f"Cannot provide single remaining applicable value ({self._applicable_value_count} candidates remaining)."
        for value in range(1, 10):
            if self._bitmask == (1 << (value - 1)):
                return value

    def is_applicable(self, value: int) -> bool:
        """
        Verifies whether the given value is applicable to the cell corresponding to this object.
        """
        value_mask = 1 << (value - 1)
        return self._bitmask & value_mask == value_mask

    def copy(self) -> _CandidateValues:
        """
        Creates and returns a deep copy of this object.
        """
        return _CandidateValues(self._bitmask, self._applicable_value_count)


class CandidateValueExclusionLogic:
    """
    Logic responsible for exclusion of candidate values inapplicable to particular cells.
    For instance, if the value of a cell is set to 5, the value 5 is excluded for all
    cells within the same row, column, and region. If a single candidate value remains
    applicable to a cell (i.e. all other candidate values have been excluded), that value
    is considered as unambiguous candidate for that cell. This class is an internal helper
    which should not be used directly by other packages.
    """

    def __init__(self, original: Optional[CandidateValueExclusionLogic] = None) -> None:
        if original:
            self._candidates = self._create_candidates_from(original)
        else:
            self._candidates = self._create_candidates_from_scratch()

    @staticmethod
    def _create_candidates_from_scratch() -> Tuple[Tuple[_CandidateValues, ...], ...]:
        rows = []
        for row in range(9):
            rows.append(tuple([_CandidateValues() for column in range(9)]))
        return tuple(rows)

    @staticmethod
    def _create_candidates_from(original: CandidateValueExclusionLogic) -> Tuple[Tuple[_CandidateValues, ...], ...]:
        rows = []
        for row in range(9):
            rows.append(tuple([original._candidates[row][column].copy() for column in range(9)]))
        return tuple(rows)

    def apply_and_exclude_cell_value(self, cell_address: CellAddress, value: int) -> Optional[List[UnambiguousCandidate]]:
        """
        Applies the given cell value to the cell with the given coordinates and excludes
        the given cell value for the peers of the cell with the coordinates.

        Args:
            cell_address (CellAddress):    The coordinates of the cell the given value is to
                                        be applied to.
            value (int):                   The value for the given cell.

        Returns:
            List of UnambiguousCandidate instances, one for each of those peers of the concerned
            cell for which just a single applicable candidate value has remained after the
            exclusion. None is returned if there is no such peer.
        """
        row, column = cell_address.row, cell_address.column
        _logger.debug("Going to apply candidate value %d to cell [%d, %d]", value, row, column)
        self._candidates[row][column].clear()
        result = None
        for peer_address in get_peer_addresses(cell_address):
            row, column = peer_address.row, peer_address.column
            _logger.debug("Going to exclude candidate value %d for cell [%d, %d]", value, row, column)
            exclusion_outcome = self._candidates[row][column].exclude_value(value)
            _logger.debug("Exclusion outcome = %s", exclusion_outcome)
            if exclusion_outcome is ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND:
                result = result or []
                candidate = UnambiguousCandidate(
                    peer_address, self._candidates[row][column].get_single_remaining_applicable_value()
                )
                result.append(candidate)
        return result

    def get_undefined_cell_candidates(self, query_mode: CandidateQueryMode) -> Optional[CandidateList]:
        """
        Returns a list of candidate values applicable to one of the undefined cells.

        Args:
            query_mode (CandidateQueryMode):    Determines the undefined cell for which the candidate
                                                values are to be provided.
        Returns:
            CandidaleList: New CandidateList instance carrying the applicable candidate values as well
                            as the address of the undefined cell the candidate values are applicable to.

        Raises:
            ValueError:   If unexpected query mode is received.
        """
        if query_mode is CandidateQueryMode.FIRST_UNDEFINED_CELL:
            return self._get_candidates_for_first_undefined_cell()
        elif query_mode is CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES:
            return self._get_candidates_for_undefined_cell_with_least_candidates()
        raise ValueError(f"Unexpected candidate query mode {query_mode}")

    def _get_candidates_for_first_undefined_cell(self) -> Optional[CandidateList]:
        for cell_address in get_all_cell_addresses():
            row, column = cell_address.row, cell_address.column
            if self._candidates[row][column].applicable_value_count > 0:
                values = self._candidates[row][column].applicable_values
                return CandidateList(cell_address, values)
        return None

    def _get_candidates_for_undefined_cell_with_least_candidates(self) -> Optional[CandidateList]:
        candidate_list = None
        for cell_address in get_all_cell_addresses():
            row, column = cell_address.row, cell_address.column
            count_for_current_cell = self._candidates[row][column].applicable_value_count
            if count_for_current_cell == 0:
                continue
            if candidate_list is None or count_for_current_cell < len(candidate_list):
                candidate_list = CandidateList(cell_address, self._candidates[row][column].applicable_values)
        return candidate_list

    def is_applicable(self, unambiguous_candidate: UnambiguousCandidate) -> bool:
        """
        Verifies whether the given unambiguous candidate is applicable.

        Args:
            unambiguous_candidate (UnambiguousCandidate): The unambiguous candidate to be verified.

        Returns:
            bool: True if and only of the candidate value carried by the given candidate
                object is applicable to the cell with the coordinates carried by the
                given candidate object. False if the concerned cell is not empty, or if
                the concerned cell value is already present in the row, column, or region
                containing the concerned cell.
        """
        cell_address = unambiguous_candidate.cell_address
        value = unambiguous_candidate.value
        return self._candidates[cell_address.row][cell_address.column].is_applicable(value)

    def get_applicable_value_count(self, cell_address: CellAddress) -> int:
        """
        Returns the number of candidate values applicable to the cell with the given
        coordinates.

        Args:
            cell_address (CellAddress):    The coordinates of the cell for which the number of
                                        applicable candidate values is to be returned.

        Returns:
            int:    The number of candidate values which are still applicable (i.e. have not
                    been excluded yet) to the cell with the given coordinates.
        """
        return self._candidates[cell_address.row][cell_address.column].applicable_value_count

    def copy(self) -> CandidateValueExclusionLogic:
        """
        Creates and returns a copy of this object which behaves as if it was a deep copy
        of this object.

        Returns:
            CandidateValueExclusionLogic: The created clone of this object. Be aware of the fact that
                                            the returned object is semantically equivalent to deep copy
                                            of this object. In other words, any modification of the clone will
                                            not change the status of this object and vice versa.
        """
        return CandidateValueExclusionLogic(self)

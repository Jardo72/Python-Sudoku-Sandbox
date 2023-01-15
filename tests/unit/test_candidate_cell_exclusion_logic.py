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

from sudoku.grid import get_cell_address
from sudoku.search.util import UnambiguousCandidate
from sudoku.search.util.candidate_cell_exclusion_logic import CandidateCellExclusionLogic, _RegionCandidateCells
from sudoku.search.util.exclusion_outcome import ExclusionOutcome


class TestRegionCandidateCells:
    """
    Test fixture aimed at the class _RegionCandidateCells.
    """

    def test_combination_of_row_and_column_exclusion_proper_candidate_is_found(self) -> None:
        """
        +-------+-------+-------+
        | 7     |       |       |
        |       |       |       |
        |       |       |     7 |
        +-------+-------+-------+
        |     7 |       |       |
        | 7     |       |       |
        |       |       | C     |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |   7   |
        +-------+-------+-------+
        For the grid above, the cell [5, 6] is the only cell in the middle right region (i.e. region
        with upper left cell [3, 6]) where the value 7 is applicable.
        """
        candidate_cells = _RegionCandidateCells(topmost_row=3, leftmost_column=6, value=7)
        
        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(0, 0), 7)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(3, 2), 7)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(8, 7), 7)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(4, 0), 7)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(2, 8), 7)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND

        expected_unambiguous_candidate = UnambiguousCandidate(get_cell_address(5, 6), 7)
        actual_unambiguous_candidate = candidate_cells.get_single_remaining_applicable_cell()
        assert expected_unambiguous_candidate == actual_unambiguous_candidate

    def test_combination_of_column_and_cell_exclusion_proper_candidate_is_found(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |   2   |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |     2 |       |       |
        +-------+-------+-------+
        | 1     |       |       |
        | C     |       |       |
        | 4     |       |       |
        +-------+-------+-------+
        For the grid above, the cell [7, 0] is the only cell in the bottom left region (i.e. region
        with upper left cell [6, 0]) where the value 2 is applicable.
        """
        candidate_cells = _RegionCandidateCells(topmost_row=6, leftmost_column=0, value=2)

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(6, 0), 1)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(1, 1), 2)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(5, 2), 2)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(8, 0), 4)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND

        expected_unambiguous_candidate = UnambiguousCandidate(get_cell_address(7, 0), 2)
        actual_unambiguous_candidate = candidate_cells.get_single_remaining_applicable_cell()
        assert expected_unambiguous_candidate == actual_unambiguous_candidate

    def test_combination_of_row_and_cell_exclusion_proper_candidate_is_found(self) -> None:
        """
        +-------+-------+-------+
        | 1 C 4 |       |       |
        |       |       |   8   |
        |       |   8   |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the cell [0, 1] is the only cell in the upper left region (i.e. region
        with upper left cell [0, 0]) where the value 8 is applicable.
        """
        candidate_cells = _RegionCandidateCells(topmost_row=0, leftmost_column=0, value=8)

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(0, 0), 1)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(1, 7), 8)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(2, 4), 8)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_NOT_FOUND

        exclusion_result = candidate_cells.apply_and_exclude_cell_value(get_cell_address(0, 2), 4)
        assert exclusion_result == ExclusionOutcome.UNAMBIGUOUS_CANDIDATE_FOUND

        expected_unambiguous_candidate = UnambiguousCandidate(get_cell_address(0, 1), 8)
        actual_unambiguous_candidate = candidate_cells.get_single_remaining_applicable_cell()
        assert expected_unambiguous_candidate == actual_unambiguous_candidate

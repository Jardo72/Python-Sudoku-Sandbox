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


class TestCandidateCellExclusionLogic:
    """
    Test fixture aimed at the CandidateCellExclusionLogic class. When designing the
    test cases, I wanted to ensure complete coverage of various aspects:
    * Exclusion of candidate cells in each of the nine regions.
    * All valid cell values.
    * Various kinds of exclusion (e.g. row and column, row and cells, column and cells).
    """

    def test_row_and_column_exclusion_with_cell_exclusion_in_upper_left_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |     9 |
        |     1 |       |       |
        |       | 9     |       |
        +-------+-------+-------+
        |   9   |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 9 has to be identified as unambiguous candidate for
        the cell [1; 0].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 8), 9)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 3), 9)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 1), 9)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 2), 1)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(1, 0), 9) in candidate_list

    def test_row_and_column_exclusion_in_upper_middle_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |     3 |
        |   3   |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       | 3     |       |
        |       |       |       |
        +-------+-------+-------+
        |       |     3 |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 3 has to be identified as unambiguous candidate for
        the cell [0; 4].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 1), 3)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 8), 3)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 3), 3)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 5), 3)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(0, 4), 3) in candidate_list

    def test_row_exclusion_with_cell_exclusion_in_upper_right_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       | 9 4   |
        | 2     |       |       |
        |       |     2 |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 2 has to be identified as unambiguous candidate for
        the cell [0; 8].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 0), 2)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 3), 2)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 6), 9)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 7), 4)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(0, 8), 2) in candidate_list

    def test_column_exclusion_with_cell_exclusion_in_middle_left_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |     4 |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |   5   |       |       |
        |       |       |       |
        |   9   |       |       |
        +-------+-------+-------+
        |       |       |       |
        | 4     |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 4 has to be identified as unambiguous candidate for
        the cell [4; 1].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 2), 4)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 0), 4)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 1), 5)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(5, 1), 9)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(4, 1), 4) in candidate_list

    def test_row_exclusion_with_cell_exclusion_in_middle_middle_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |   5   |       |       |
        |       | 2   7 |       |
        |       |       |     5 |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 5 has to be identified as unambiguous candidate for
        the cell [4; 4].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 1), 5)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(5, 8), 5)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 3), 2)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 5), 7)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(4, 4), 5) in candidate_list

    def test_row_and_column_exclusion_with_cell_exclusion_in_middle_right_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |   8   |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       | 5     |
        |       |       |       |
        |     8 |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |     8 |
        +-------+-------+-------+
        For the grid above, the value 8 has to be identified as unambiguous candidate for
        the cell [4; 6].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 7), 8)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(5, 2), 8)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(8, 8), 8)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 6), 5)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(4, 6), 8) in candidate_list

    def test_row_and_column_exclusion_in_bottom_left_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        | 7     |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |     7 |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |   7   |
        |       |       |       |
        |       | 7     |       |
        +-------+-------+-------+
        For the grid above, the value 7 has to be identified as unambiguous candidate for
        the cell [7; 1].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 0), 7)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 2), 7)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 7), 7)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(8, 3), 7)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(7, 1), 7) in candidate_list

    def test_column_exclusion_with_cell_exclusion_in_bottom_middle_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       | 6     |       |
        |       |       |       |
        +-------+-------+-------+
        |       |   6   |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |     3 |       |
        |       |     8 |       |
        +-------+-------+-------+
        For the grid above, the value 6 has to be identified as unambiguous candidate for
        the cell [6; 5].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 3), 6)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 4), 6)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 5), 3)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(8, 5), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(6, 5), 6) in candidate_list

    def test_row_and_column_exclusion_with_cell_exclusion_in_bottom_right_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |     1 |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |   8   |
        |   1   |       |       |
        |       | 1     |       |
        +-------+-------+-------+
        For the grid above, the value 1 has to be identified as unambiguous candidate for
        the cell [6; 6].
        """
        exclusion_logic = CandidateCellExclusionLogic()

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 8), 1)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 1), 1)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(8, 3), 1)
        assert candidate_list is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 7), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(6, 6), 1) in candidate_list

    def test_clone_reflects_the_state_of_the_original_when_further_exclusion_is_performed(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       | 4     |       |
        |       |       |       |
        +-------+-------+-------+
        |   4   |       |       |
        |       |     1 |       |
        |       |   7 2 |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 4 has to be identified as unambiguous candidate for
        the cell [4; 4], even if half of the exclusion is performed with one instance of
        exclusion logic, and the other half is performed with a clone of the above mentioned
        instance. The unambiguous candidate is identified by the clone. The original instance
        cannot identify any unambiguous candidate.
        """
        original = CandidateCellExclusionLogic()

        original.apply_and_exclude_cell_value(get_cell_address(1, 3), 4)
        original.apply_and_exclude_cell_value(get_cell_address(4, 5), 1)
        original.apply_and_exclude_cell_value(get_cell_address(5, 4), 7)

        clone = original.copy()
        clone.apply_and_exclude_cell_value(get_cell_address(3, 1), 4)

        candidate_list = clone.apply_and_exclude_cell_value(get_cell_address(5, 5), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(4, 4), 4) in candidate_list

    def test_exclusion_in_clone_does_not_affect_the_original(self) -> None:
        """
        If a clone of exclusion logic is created after several exclusions, further exclusions
        performed upon the clone will not affect the original exclusion logic.
        """
        original = CandidateCellExclusionLogic()

        original.apply_and_exclude_cell_value(get_cell_address(1, 3), 4)
        original.apply_and_exclude_cell_value(get_cell_address(4, 5), 1)
        original.apply_and_exclude_cell_value(get_cell_address(5, 4), 7)

        clone = original.copy()
        clone.apply_and_exclude_cell_value(get_cell_address(3, 1), 4)

        candidate_list = original.apply_and_exclude_cell_value(get_cell_address(5, 5), 2)
        assert candidate_list is None

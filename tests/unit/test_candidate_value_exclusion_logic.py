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

from sudoku.grid import CellAddress
from sudoku.grid import get_cell_address
from sudoku.search.util import CandidateList
from sudoku.search.util import CandidateQueryMode
from sudoku.search.util import UnambiguousCandidate
from sudoku.search.util.candidate_value_exclusion_logic import CandidateValueExclusionLogic


class TestCandidateValueExclusionLogic:
    """
    Test fixture aimed at the sudoku.grid.CandidateValueExclusionLogic class. When designing
    the test cases, I wanted to ensure complete coverage of various aspects:
    * Various kinds of exclusion (pure row exclusion, pure column exclusion, pure region
      exclusion, various combinations like row and column exclusion).
    * Equivalence classes and (implicit) boundary values (i.e. top/bottom row,
      leftmost/rightmost column, regions).
    * All valid cell values.
    """

    def test_pure_row_exclusion_in_topmost_row_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        | 9 6 5 | 8 7 4 |   1 3 |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 2 has to be identified as unambiguous candidate
        for the cell [0; 6].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=2), 5) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=0), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=7), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=4), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=1), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=8), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=3), 8) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=5), 4)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=0, column=6), 2) in candidate_list

    def test_pure_row_exclusion_in_bottom_row_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        | 7 6   | 2 4 8 | 1 3 9 |
        +-------+-------+-------+
        For the grid above, the value 5 has to be identified as unambiguous candidate
        for the cell [8; 2].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=7), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=0), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=3), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=8), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=1), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=6), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=4), 4) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=5), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=8, column=2), 5) in candidate_list

    def test_pure_column_exclusion_in_leftmost_column_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        | 3     |       |       |
        | 7     |       |       |
        | 1     |       |       |
        +-------+-------+-------+
        | 9     |       |       |
        | 2     |       |       |
        | 6     |       |       |
        +-------+-------+-------+
        |       |       |       |
        | 5     |       |       |
        | 8     |       |       |
        +-------+-------+-------+
        For the grid above, the value 4 has to be identified as unambiguous candidate
        for the cell [6; 0].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=0), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=0), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=0), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=0), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=0), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=0), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=0), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=0), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=6, column=0), 4) in candidate_list

    def test_pure_column_exclusion_in_rightmost_column_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |     2 |
        |       |       |     7 |
        |       |       |     5 |
        +-------+-------+-------+
        |       |       |     9 |
        |       |       |     4 |
        |       |       |     3 |
        +-------+-------+-------+
        |       |       |     6 |
        |       |       |     8 |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 1 has to be identified as unambiguous candidate
        for the cell [8; 8].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=8), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=8), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=8), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=8), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=8), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=8), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=8), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=8), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=8, column=8), 1) in candidate_list

    def test_pure_region_exclusion_in_upper_left_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        | 3 1 6 |       |       |
        | 9 2 4 |       |       |
        | 8   5 |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 7 has to be identified as unambiguous candidate
        for the cell [2; 1].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=0), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=2), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=1), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=0), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=2), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=1), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=2), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=0), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=2, column=1), 7) in candidate_list

    def test_pure_region_exclusion_in_upper_right_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       | 9 1   |
        |       |       | 2 7 3 |
        |       |       | 4 5 8 |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 6 has to be identified as unambiguous candidate
        for the cell [0; 8].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=7), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=8), 3) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=6), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=6), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=6), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=7), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=7), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=8), 8)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=0, column=8), 6) in candidate_list

    def test_pure_region_exclusion_in_bottom_left_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        | 9 1 5 |       |       |
        | 6   2 |       |       |
        | 3 4 7 |       |       |
        +-------+-------+-------+
        For the grid above, the value 8 has to be identified as unambiguous candidate
        for the cell [7; 1].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=1), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=1), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=0), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=2), 2) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=0), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=2), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=2), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=0), 3)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=7, column=1), 8) in candidate_list

    def test_pure_region_exclusion_in_bottom_right_region_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       | 5 7 1 |
        |       |       | 8 2 9 |
        |       |       | 6 4   |
        +-------+-------+-------+
        For the grid above, the value 3 has to be identified as unambiguous candidate
        for the cell [8; 8].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=6), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=6), 8) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=8), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=8), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=7), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=7), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=6), 5) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=7), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=8, column=8), 3) in candidate_list

    def test_combination_of_row_and_column_exclusion_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       | 9     |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       | 2     |       |
        |   3   |     5 | 1   8 |
        |       |       |       |
        +-------+-------+-------+
        |       | 4     |       |
        |       | 7     |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 6 has to be identified as unambiguous candidate
        for the cell [4; 3].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=5), 5) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=8), 8) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=6), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=3), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=3), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=3), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=1), 3) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=3), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=4, column=3), 6) in candidate_list

    def test_combination_of_row_and_region_exclusion_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        | 7   3 |     2 |   8 5 |
        |       |       |   1   |
        |       |       | 6   4 |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 9 has to be identified as unambiguous candidate
        for the cell [3; 6].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=8), 5) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=7), 8) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=7), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=6), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=8), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=0), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=2), 3) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=5), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=3, column=6), 9) in candidate_list

    def test_combination_of_column_and_region_exclusion_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       | 3     |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       | 7   9 |       |
        |       |   5   |       |
        |       | 4 8   |       |
        +-------+-------+-------+
        |       | 6     |       |
        |       | 2     |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the value 1 has to be identified as unambiguous candidate
        for the cell [4; 3].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=5), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=4), 8) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=4), 5) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=3), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=3), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=3), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=3), 3) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=3), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=4, column=3), 1) in candidate_list

    def test_combination_of_row_and_column_and_region_exlusion_finds_proper_unambiguous_candidate(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |     4 |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |     1 |       |       |
        |       |       |       |
        +-------+-------+-------+
        |   2   |   7   |     6 |
        | 5     |       |       |
        |   9 3 |       |       |
        +-------+-------+-------+
        For the grid above, the value 8 has to be identified as unambiguous candidate
        for the cell [6; 2].
        """
        exclusion_logic = CandidateValueExclusionLogic()

        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=1), 9) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=2), 1) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=0), 5) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=8), 6) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=2), 4) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=4), 7) is None
        assert exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=2), 3) is None

        candidate_list = exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=1), 2)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(CellAddress(row=6, column=2), 8) in candidate_list

    def test_candidates_for_first_undefined_cell_reflect_exclusion(self) -> None:
        """
        +-------+-------+-------+
        |       | 7     |       |
        |   9   |       |       |
        |   4   |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        | 2     |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        For the grid above, the values 1, 3, 5, 6 and 8 have to be identified as candidates
        for the cell [0; 0], which should be identified as the first undefined cell.
        """
        exclusion_logic = CandidateValueExclusionLogic()

        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=3), 7)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=0), 2)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=1), 9)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=1), 4)

        actual_candidate_list = exclusion_logic.get_undefined_cell_candidates(CandidateQueryMode.FIRST_UNDEFINED_CELL)
        expected_candidate_list = CandidateList(CellAddress(row=0, column=0), (1, 3, 5, 6, 8))
        assert actual_candidate_list == expected_candidate_list

    def test_candidates_for_undefined_cell_with_least_candidates_reflect_exclusion(self) -> None:
        """
        +-------+-------+-------+
        |       | 7     |       |
        |   9   |       |     3 |
        |   4   |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |     2 |
        | 2     |       |       |
        +-------+-------+-------+
        |       |       | 7     |
        |       |       |     1 |
        |     5 |     9 |       |
        +-------+-------+-------+
        For the grid above, the values 4, 6 and 8 have to be identified as candidates
        for the cell [8; 8], which should be identified as the undefined cells with
        least candidate.
        """
        exclusion_logic = CandidateValueExclusionLogic()

        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=0, column=3), 7)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=1), 9)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=1, column=8), 3)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=2, column=1), 4)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=4, column=8), 2)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=5, column=0), 2)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=6, column=6), 7)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=7, column=8), 1)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=2), 5)
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=8, column=5), 9)

        actual_candidate_list = exclusion_logic.get_undefined_cell_candidates(CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES)
        expected_candidate_list = CandidateList(CellAddress(row=8, column=8), (4, 6, 8))
        assert actual_candidate_list == expected_candidate_list

    def test_no_value_is_applicable_to_cell_whose_value_has_been_already_set(self) -> None:
        exclusion_logic = CandidateValueExclusionLogic()
        exclusion_logic.apply_and_exclude_cell_value(CellAddress(row=3, column=2), 5)
        for value in range(1, 10):
            candidate = UnambiguousCandidate(CellAddress(row=3, column=2), value)
            assert not exclusion_logic.is_applicable(candidate)

    def test_applicability_of_value_reflects_former_exclusions(self) -> None:
        exclusion_logic = CandidateValueExclusionLogic()
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 5), 9)
        assert exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(0, 4), 8))
        assert not exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(0, 4), 9))

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 5), 6)
        assert exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(1, 5), 3))
        assert not exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(1, 5), 6))

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 0), 5)
        assert exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(5, 1), 3))
        assert not exclusion_logic.is_applicable(UnambiguousCandidate(get_cell_address(5, 1), 5))

    def test_number_of_applicable_values_reflects_exclusion(self) -> None:
        exclusion_logic = CandidateValueExclusionLogic()
        assert exclusion_logic.get_applicable_value_count(get_cell_address(0, 0)) == 9

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 0), 1)
        assert exclusion_logic.get_applicable_value_count(get_cell_address(0, 0)) == 0
        assert exclusion_logic.get_applicable_value_count(get_cell_address(0, 1)) == 8
        assert exclusion_logic.get_applicable_value_count(get_cell_address(1, 0)) == 8

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 1), 3)
        assert exclusion_logic.get_applicable_value_count(get_cell_address(1, 1)) == 0
        assert exclusion_logic.get_applicable_value_count(get_cell_address(0, 1)) == 7
        assert exclusion_logic.get_applicable_value_count(get_cell_address(1, 0)) == 7

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 2), 9)
        assert exclusion_logic.get_applicable_value_count(get_cell_address(2, 2)) == 0
        assert exclusion_logic.get_applicable_value_count(get_cell_address(0, 1)) == 6
        assert exclusion_logic.get_applicable_value_count(get_cell_address(1, 0)) == 6

    def test_clone_reflects_the_state_of_the_original_when_candidates_are_requested(self) -> None:
        """
        +-------+-------+-------+
        | 2     | 7     | 1     |
        |     4 |       |     3 |
        |   8   |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |     2 |       |       |
        +-------+-------+-------+
        |       |       | 7     |
        |   3 5 |     9 |   2 4 |
        |       |       |       |
        +-------+-------+-------+
        For the grid above:
        * The cell [0; 1] is to be identified as the first undefined cell. The applicable
          candidates for that cell should be 5, 6, and 9.
        * The cell [7; 6] is to be identified as undefined cell with least candidates. The
          applicable candidates for that cell should be 6 and 8.
        A clone of the corresponding exclusion logic has to identify the same candidate
        values.
        """
        exclusion_logic = CandidateValueExclusionLogic()
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 0), 2)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 3), 7)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(0, 6), 1)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 2), 4)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 8), 3)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(2, 1), 8)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 2), 2)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 6), 7)

        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 1), 3)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 2), 5)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 5), 9)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 7), 2)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(7, 8), 4)

        clone = exclusion_logic.copy()

        actual_candidate_list = clone.get_undefined_cell_candidates(CandidateQueryMode.FIRST_UNDEFINED_CELL)
        expected_candidate_list = CandidateList(get_cell_address(0, 1), (5, 6, 9))
        assert expected_candidate_list == expected_candidate_list

        actual_candidate_list = clone.get_undefined_cell_candidates(CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES)
        expected_candidate_list = CandidateList(get_cell_address(7, 6), (6, 8))
        assert expected_candidate_list == actual_candidate_list

    def test_clone_reflects_the_state_of_the_original_when_further_exclusion_is_performed(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |   5   |       |
        |       |       |       |
        +-------+-------+-------+
        |       | 1     |       |
        | 6     |     3 |   2   |
        |       | 7     |       |
        +-------+-------+-------+
        |       |   8   |       |
        |       |       |       |
        |       |   9   |       |
        +-------+-------+-------+
        For the grid above, value 4 is to be identified as unambiguous candidate for the
        cell [4; 4], even if half of the exclusion is performed with one instance of
        exclusion logic, and the other half is performed with a clone of the above mentioned
        instance. The unambiguous candidate is identified by the clone. The original instance
        cannot identify any unambiguous candidate.
        """
        exclusion_logic = CandidateValueExclusionLogic()
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(1, 4), 5)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(3, 3), 1)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 0), 6)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 7), 2)

        clone = exclusion_logic.copy()
        clone.apply_and_exclude_cell_value(get_cell_address(4, 5), 3)
        clone.apply_and_exclude_cell_value(get_cell_address(5, 3), 7)
        clone.apply_and_exclude_cell_value(get_cell_address(6, 4), 8)

        candidate_list = clone.apply_and_exclude_cell_value(get_cell_address(8, 4), 9)
        assert len(candidate_list) == 1
        assert UnambiguousCandidate(get_cell_address(4, 4), 4) in candidate_list

    def test_exclusion_in_clone_does_not_affect_the_original(self) -> None:
        """
        +-------+-------+-------+
        |       |       |       |
        |       |       |       |
        |       |       |       |
        +-------+-------+-------+
        |       |       |       |
        |       |     3 |       |
        |       | 7     |       |
        +-------+-------+-------+
        |       |   8   |       |
        |       |       |       |
        |       |   9   |       |
        +-------+-------+-------+
        For the grid above, the values 1, 2, 4, 5 and 6 have to be identified as candidates
        for the cell [3; 4]. The above mentioned cell should be identified as undefined cell
        with least candidates for the original exclusion logic instance, depsite of further
        exclusions performed with a clone of the exclusion logic.
        """
        exclusion_logic = CandidateValueExclusionLogic()
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(4, 5), 3)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(5, 3), 7)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(6, 4), 8)
        exclusion_logic.apply_and_exclude_cell_value(get_cell_address(8, 4), 9)

        clone = exclusion_logic.copy()
        clone.apply_and_exclude_cell_value(get_cell_address(1, 4), 5)
        clone.apply_and_exclude_cell_value(get_cell_address(3, 3), 1)
        clone.apply_and_exclude_cell_value(get_cell_address(4, 7), 2)

        actual_candidate_list = exclusion_logic.get_undefined_cell_candidates(CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES)
        expected_candidate_list = CandidateList(get_cell_address(3, 4), (1, 2, 4, 5, 6))
        assert expected_candidate_list == actual_candidate_list

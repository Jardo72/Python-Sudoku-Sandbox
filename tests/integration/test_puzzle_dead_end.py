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

from pytest import mark

from sudoku.search.engine import SearchOutcome

from commons import TestSearchEngine


_algorithms = ["UCS", "Smart-BFS", "Naive-BFS", "Smart-DFS", "Naive-DFS"]


class TestPuzzleDeadEnd:
    """
    Collection of integration tests covering the case when the search leads to puzzle dead end.
    """

    @mark.parametrize("algorithm_name", _algorithms)
    def test_puzzle_with_empty_cell_for_which_all_cell_values_are_excluded_by_row_and_column_puzzle_dead_end(self, algorithm_name: str) -> None:  # noqa: E501
        puzzle = """
+-------+-------+-------+
| 1   7 |   2   | 9   4 |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       | 3     |       |
|       | 8     |       |
|       |       |       |
+-------+-------+-------+
|       | 6     |       |
|       |       |       |
|       | 5     |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.PUZZLE_DEAD_END
        assert test_summary.search_summary.algorithm == algorithm_name

    @mark.parametrize("algorithm_name", _algorithms)
    def test_puzzle_with_empty_cell_for_which_all_cell_values_are_excluded_by_row_and_region_puzzle_dead_end(self, algorithm_name: str) -> None:  # noqa: E501
        puzzle = """
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
| 7   5 | 3   9 |   1 2 |
|       | 8   4 |       |
|       | 6 5   |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.PUZZLE_DEAD_END
        assert test_summary.search_summary.algorithm == algorithm_name

    @mark.parametrize("algorithm_name", _algorithms)
    def test_puzzle_with_empty_cell_for_which_all_cell_values_are_excluded_by_column_and_region_puzzle_dead_end(self, algorithm_name: str) -> None:  # noqa: E501
        puzzle = """
+-------+-------+-------+
|       |       |       |
|       |       | 6     |
|       |       | 3     |
+-------+-------+-------+
|       |       | 9     |
|       |       |       |
|       |       | 1     |
+-------+-------+-------+
|       |       |       |
|       |       | 2   4 |
|       |       | 5 7 8 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.PUZZLE_DEAD_END
        assert test_summary.search_summary.algorithm == algorithm_name

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

from sudoku.search.engine import SearchOutcome

from commons import TestSearchEngine
from commons import _assert_are_equivalent


class TestAlgorithmDeadEnd:
    """
    Collection of integration tests covering the case when the search leads to
    algorithm dead end.
    """

    def test_case_01(self) -> None:
        puzzle = """
+-------+-------+-------+
|   7 6 |   3 9 | 4 8 5 |
| 1     |       |       |
| 3     |     7 |       |
+-------+-------+-------+
| 8     |     5 |   4 9 |
| 6     |     3 | 2 7 8 |
| 5     |       |       |
+-------+-------+-------+
| 9     |     2 |       |
| 4     |     8 |       |
| 7     |     4 |       |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
| 2 7 6 | 1 3 9 | 4 8 5 |
| 1     |     6 |       |
| 3     |     7 |       |
+-------+-------+-------+
| 8     |     5 |   4 9 |
| 6     |     3 | 2 7 8 |
| 5     |     1 |       |
+-------+-------+-------+
| 9     |     2 |       |
| 4     |     8 |       |
| 7     |     4 |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_02(self) -> None:
        puzzle = """
+-------+-------+-------+
|       | 4   6 | 5     |
| 1     |     8 |     9 |
|       |   9   |       |
+-------+-------+-------+
|       |   6 5 |   9 1 |
| 7     |   8   | 3     |
|       | 1     |   5 2 |
+-------+-------+-------+
|   5   | 3   4 | 2   8 |
| 6     |       |     4 |
| 4     |       |   1   |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
|       | 4   6 | 5     |
| 1     |     8 |     9 |
|       |   9   |       |
+-------+-------+-------+
|       |   6 5 |   9 1 |
| 7     |   8   | 3 4 6 |
|       | 1     |   5 2 |
+-------+-------+-------+
| 9 5   | 3   4 | 2   8 |
| 6     |       |     4 |
| 4     |       |   1   |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_03(self) -> None:
        puzzle = """
+-------+-------+-------+
|       |     4 | 6     |
|       |   8   |     4 |
| 7 4   |   6   | 1     |
+-------+-------+-------+
|   8   | 5     |       |
| 1 9 6 |       | 7 3 5 |
|       |     6 |   2   |
+-------+-------+-------+
|     8 |   9   |   4 2 |
| 5     |   7   |       |
|     1 | 3     |       |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
|       |     4 | 6     |
|       |   8   |     4 |
| 7 4   |   6   | 1     |
+-------+-------+-------+
|   8   | 5     |       |
| 1 9 6 |       | 7 3 5 |
|       |     6 |   2   |
+-------+-------+-------+
|     8 |   9   |   4 2 |
| 5     |   7   |       |
|     1 | 3     |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_04(self) -> None:
        puzzle = """
+-------+-------+-------+
|       |     3 | 4     |
| 3     |   6   |       |
|       |     4 |       |
+-------+-------+-------+
|       | 7 1 5 |     2 |
|   4   |       |       |
| 9   2 |   8   | 3     |
+-------+-------+-------+
|     4 | 3     |       |
|       |     2 |       |
|       |   9   |     4 |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
|       |     3 | 4     |
| 3     |   6   |       |
|       |     4 |       |
+-------+-------+-------+
|       | 7 1 5 |     2 |
|   4   | 2 3 9 |       |
| 9   2 | 4 8 6 | 3     |
+-------+-------+-------+
|     4 | 3     |       |
|       |     2 |       |
|       |   9   |     4 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_05(self) -> None:
        puzzle = """
+-------+-------+-------+
|       | 4   9 |       |
| 7   1 |       |   8   |
|       | 3     | 9     |
+-------+-------+-------+
|       |       |   5 9 |
| 2     |   5 7 |     1 |
| 3 9   |     8 |       |
+-------+-------+-------+
|     9 |   2 3 |   1   |
|       |   9   |   4   |
|       | 6     |       |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
|       | 4   9 |       |
| 7   1 |   6   |   8   |
|       | 3     | 9     |
+-------+-------+-------+
|       |       |   5 9 |
| 2     | 9 5 7 |     1 |
| 3 9   |     8 |       |
+-------+-------+-------+
|     9 |   2 3 |   1   |
|       |   9   |   4   |
|       | 6     |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_06(self) -> None:
        puzzle = """
+-------+-------+-------+
|       |       |   7 2 |
| 1     |       | 4     |
| 7     |     2 |       |
+-------+-------+-------+
| 6     | 7     |   1 5 |
|     2 |       |       |
|       |     5 | 9   7 |
+-------+-------+-------+
|   5 7 |       | 2     |
|     4 | 8 1   |       |
|     9 |     7 | 3     |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
|       |       |   7 2 |
| 1     |       | 4     |
| 7     |     2 |       |
+-------+-------+-------+
| 6   3 | 7     | 8 1 5 |
|     2 |       | 6     |
|       |     5 | 9   7 |
+-------+-------+-------+
|   5 7 |       | 2     |
|     4 | 8 1   |       |
|     9 |     7 | 3     |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

    def test_case_07(self) -> None:
        puzzle = """
+-------+-------+-------+
| 1     |       |       |
|   2   |       |       |
|     3 |       |       |
+-------+-------+-------+
|       | 4     |       |
|       |   5   |       |
|       |     6 |       |
+-------+-------+-------+
|       |       | 7     |
|       |       |   8   |
|       |       |     9 |
+-------+-------+-------+
"""
        expected_final_grid = """
+-------+-------+-------+
| 1     |       |       |
|   2   |       |       |
|     3 |       |       |
+-------+-------+-------+
|       | 4     |       |
|       |   5   |       |
|       |     6 |       |
+-------+-------+-------+
|       |       | 7     |
|       |       |   8   |
|       |       |     9 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, "UCS")

        assert test_summary.search_summary.outcome == SearchOutcome.ALGORITHM_DEAD_END
        _assert_are_equivalent(expected_final_grid, test_summary.final_grid)

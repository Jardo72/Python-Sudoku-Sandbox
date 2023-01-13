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
from commons import _assert_are_equivalent


_algorithms = ["UCS", "Smart-DFS", "Smart-BFS", "Naive-DFS", "Naive-BFS"]

_DURATION_MILLIS = 50


class TestSimplePuzzleSolutionFoundEvenByNaiveAlgorithm:
    """
    Collection of integration tests covering the case when a very simple puzzle is successfully
    solved by various search algorithms including naive ones.
    """

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_01(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
|   8 5 | 1 3 4 | 9 6 7 |
| 6 7 1 | 2   8 | 3 5 4 |
| 3 9 4 | 6 5 7 | 2 8   |
+-------+-------+-------+
| 7   3 | 4 2 9 | 6 1   |
| 8 6 2 | 5 1   |   7 9 |
| 4 1   | 7 8 6 | 5 2 3 |
+-------+-------+-------+
| 5 2 7 | 3 4 1 | 8 9 6 |
| 9 4 6 |   7 5 | 1 3 2 |
|   3 8 | 9 6 2 | 7   5 |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 2 8 5 | 1 3 4 | 9 6 7 |
| 6 7 1 | 2 9 8 | 3 5 4 |
| 3 9 4 | 6 5 7 | 2 8 1 |
+-------+-------+-------+
| 7 5 3 | 4 2 9 | 6 1 8 |
| 8 6 2 | 5 1 3 | 4 7 9 |
| 4 1 9 | 7 8 6 | 5 2 3 |
+-------+-------+-------+
| 5 2 7 | 3 4 1 | 8 9 6 |
| 9 4 6 | 8 7 5 | 1 3 2 |
| 1 3 8 | 9 6 2 | 7 4 5 |
+-------+-------+-------+"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 11
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_02(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 2 9   |   5 3 | 8 1 6 |
| 6 8 5 | 4 1 2 |   3 7 |
|   7 1 | 9   8 | 2 5 4 |
+-------+-------+-------+
| 5 4 7 | 2   9 | 1 6 3 |
| 8 6 3 | 1 4 7 | 5 9   |
|   1 2 | 6 3 5 |   7 8 |
+-------+-------+-------+
| 4 5 9 | 3 2 6 | 7 8 1 |
| 1 3   |   7 4 | 6 2 9 |
| 7   6 | 8 9 1 |     5 |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 2 9 4 | 7 5 3 | 8 1 6 |
| 6 8 5 | 4 1 2 | 9 3 7 |
| 3 7 1 | 9 6 8 | 2 5 4 |
+-------+-------+-------+
| 5 4 7 | 2 8 9 | 1 6 3 |
| 8 6 3 | 1 4 7 | 5 9 2 |
| 9 1 2 | 6 3 5 | 4 7 8 |
+-------+-------+-------+
| 4 5 9 | 3 2 6 | 7 8 1 |
| 1 3 8 | 5 7 4 | 6 2 9 |
| 7 2 6 | 8 9 1 | 3 4 5 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 14
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_03(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 5 6 8 |   9 2 |   3 4 |
| 1 3 7 | 8 4 6 | 5 9 2 |
| 9   2 | 7 5   | 8 1   |
+-------+-------+-------+
| 2 9   | 3 7 5 | 6 8 1 |
| 8 1 3 | 2   9 | 4 5 7 |
| 6   5 | 4 1 8 | 9 2   |
+-------+-------+-------+
| 4   1 |   3 7 | 2 6 9 |
| 3 5 9 | 6 2 4 | 1 7 8 |
| 7 2 6 | 9 8   |     5 |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 5 6 8 | 1 9 2 | 7 3 4 |
| 1 3 7 | 8 4 6 | 5 9 2 |
| 9 4 2 | 7 5 3 | 8 1 6 |
+-------+-------+-------+
| 2 9 4 | 3 7 5 | 6 8 1 |
| 8 1 3 | 2 6 9 | 4 5 7 |
| 6 7 5 | 4 1 8 | 9 2 3 |
+-------+-------+-------+
| 4 8 1 | 5 3 7 | 2 6 9 |
| 3 5 9 | 6 2 4 | 1 7 8 |
| 7 2 6 | 9 8 1 | 3 4 5 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 14
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_04(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 3 5 7 | 6 9 1 |   4 8 |
|   8 2 |   3 5 | 6 9 1 |
| 1 6 9 | 4 2 8 | 7 3   |
+-------+-------+-------+
|   4 3 | 8 5 9 |   6 7 |
| 9 7 8 | 1   4 | 3   2 |
| 6 1 5 | 2 7   | 4 8 9 |
+-------+-------+-------+
| 7 3   | 5 8 6 |   2 4 |
|   2 6 | 9 4   | 5 1 3 |
| 5 9 4 | 3 1 2 | 8 7 6 |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 3 5 7 | 6 9 1 | 2 4 8 |
| 4 8 2 | 7 3 5 | 6 9 1 |
| 1 6 9 | 4 2 8 | 7 3 5 |
+-------+-------+-------+
| 2 4 3 | 8 5 9 | 1 6 7 |
| 9 7 8 | 1 6 4 | 3 5 2 |
| 6 1 5 | 2 7 3 | 4 8 9 |
+-------+-------+-------+
| 7 3 1 | 5 8 6 | 9 2 4 |
| 8 2 6 | 9 4 7 | 5 1 3 |
| 5 9 4 | 3 1 2 | 8 7 6 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 13
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_05(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
|   6 2 |   5 7 | 1 9   |
| 1 5   | 3 8   | 4 2 6 |
| 8 4 9 | 2 1 6 | 7 3   |
+-------+-------+-------+
| 2 9 4 | 7 6 1 | 8 5   |
|   1 3 |   2 5 | 9 7 4 |
| 7 8   | 9 4 3 | 6 1 2 |
+-------+-------+-------+
|   3 6 | 1 9 4 |   8 7 |
| 4 2 1 | 5   8 | 3 6 9 |
|   7 8 | 6   2 | 5 4   |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 3 6 2 | 4 5 7 | 1 9 8 |
| 1 5 7 | 3 8 9 | 4 2 6 |
| 8 4 9 | 2 1 6 | 7 3 5 |
+-------+-------+-------+
| 2 9 4 | 7 6 1 | 8 5 3 |
| 6 1 3 | 8 2 5 | 9 7 4 |
| 7 8 5 | 9 4 3 | 6 1 2 |
+-------+-------+-------+
| 5 3 6 | 1 9 4 | 2 8 7 |
| 4 2 1 | 5 7 8 | 3 6 9 |
| 9 7 8 | 6 3 2 | 5 4 1 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 16
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_06(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 3 9   |   5 2 | 6 7 8 |
| 2 6 4 | 1 8 7 | 5   9 |
| 8   7 |   6 3 | 2 1 4 |
+-------+-------+-------+
| 5 4 9 | 3   1 | 8 6 2 |
|   2 8 | 6 9 4 | 1 5 3 |
| 1 3 6 | 8 2 5 | 4 9   |
+-------+-------+-------+
|   7 2 | 5   9 | 3 8 1 |
| 9 1 5 |   3   | 7 4 6 |
| 4 8   | 7 1 6 |   2   |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 3 9 1 | 4 5 2 | 6 7 8 |
| 2 6 4 | 1 8 7 | 5 3 9 |
| 8 5 7 | 9 6 3 | 2 1 4 |
+-------+-------+-------+
| 5 4 9 | 3 7 1 | 8 6 2 |
| 7 2 8 | 6 9 4 | 1 5 3 |
| 1 3 6 | 8 2 5 | 4 9 7 |
+-------+-------+-------+
| 6 7 2 | 5 4 9 | 3 8 1 |
| 9 1 5 | 2 3 8 | 7 4 6 |
| 4 8 3 | 7 1 6 | 9 2 5 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 15
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_07(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 3 9 2 |   4 5 | 7 6 8 |
| 4 5 6 | 8 2 7 | 1   9 |
| 7 1   | 9 6 3 | 5 2   |
+-------+-------+-------+
| 6 8 9 | 7 5 1 | 2 4 3 |
|   4 3 |   8 9 |   1   |
| 1 2   |   3 6 | 8 9 5 |
+-------+-------+-------+
| 9 7   | 5 1   | 3   6 |
| 2 3 5 | 6 9 8 | 4 7 1 |
| 8 6   | 3 7 4 |   5 2 |
+-------+-------+-------+
"""
        expected_solution = """
+-------+-------+-------+
| 3 9 2 | 1 4 5 | 7 6 8 |
| 4 5 6 | 8 2 7 | 1 3 9 |
| 7 1 8 | 9 6 3 | 5 2 4 |
+-------+-------+-------+
| 6 8 9 | 7 5 1 | 2 4 3 |
| 5 4 3 | 2 8 9 | 6 1 7 |
| 1 2 7 | 4 3 6 | 8 9 5 |
+-------+-------+-------+
| 9 7 4 | 5 1 2 | 3 8 6 |
| 2 3 5 | 6 9 8 | 4 7 1 |
| 8 6 1 | 3 7 4 | 9 5 2 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name)

        assert test_summary.search_summary.outcome == SearchOutcome.SOLUTION_FOUND
        assert test_summary.search_summary.algorithm == algorithm_name
        assert test_summary.search_summary.cell_values_tried == 15
        assert test_summary.search_summary.duration_millis < _DURATION_MILLIS
        _assert_are_equivalent(expected_solution, test_summary.final_grid)

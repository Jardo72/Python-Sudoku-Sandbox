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


_algorithms = ["Naive-DFS", "Naive-BFS"]


_TIMEOUT_SEC = 1


class TestAmbiguousPuzzlesLeadingToTimeout:
    """
    Collection of integration tests covering the case when a search fails because of timeout.
    """

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_01(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
|   7   |       |   1   |
| 5     |     6 |     7 |
|     1 |   8   | 5     |
+-------+-------+-------+
|   2   |       |   7   |
|       |   2   |       |
|   3   |       |   9   |
+-------+-------+-------+
|       |   9   | 8     |
| 9     | 6   4 |     3 |
|   5   |       |     4 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name, timeout_sec=_TIMEOUT_SEC)

        assert test_summary.search_summary.outcome == SearchOutcome.TIMEOUT
        assert test_summary.search_summary.duration_millis >= _TIMEOUT_SEC * 1000
        assert test_summary.search_summary.algorithm == algorithm_name

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_02(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
|       |   3   |       |
| 9     | 7     | 6     |
| 7     |   1   |   8 3 |
+-------+-------+-------+
|       |   4 1 | 7   6 |
| 4   9 |   7   |     5 |
|       |     3 |       |
+-------+-------+-------+
|   6   |       | 1 9   |
|     3 |     7 |       |
| 8     |       | 4   7 |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name, timeout_sec=_TIMEOUT_SEC)

        assert test_summary.search_summary.outcome == SearchOutcome.TIMEOUT
        assert test_summary.search_summary.duration_millis >= _TIMEOUT_SEC * 1000
        assert test_summary.search_summary.algorithm == algorithm_name

    @mark.parametrize("algorithm_name", _algorithms)
    def test_case_03(self, algorithm_name: str) -> None:
        puzzle = """
+-------+-------+-------+
| 7     |   2   |   5   |
|       | 3     | 4     |
|     1 |       |       |
+-------+-------+-------+
| 2     |   5 9 |       |
|   8   |       | 1   4 |
|       |       |       |
+-------+-------+-------+
| 5 3   |       |   9   |
|       | 4     | 6     |
|       |       |       |
+-------+-------+-------+
"""
        test_summary = TestSearchEngine.find_solution(puzzle, algorithm_name, timeout_sec=_TIMEOUT_SEC)

        assert test_summary.search_summary.outcome == SearchOutcome.TIMEOUT
        assert test_summary.search_summary.duration_millis >= _TIMEOUT_SEC * 1000
        assert test_summary.search_summary.algorithm == algorithm_name

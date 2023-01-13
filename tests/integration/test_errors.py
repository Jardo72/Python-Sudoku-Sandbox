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

from pytest import raises

from sudoku.search.engine import InvalidPuzzleError, NoSuchAlgorithmError

from commons import TestSearchEngine


class TestErrors:
    """
    Collection of integration tests covering the case when a puzzle is rejected by the search
    engine, for instance if it is an invalid puzzle, or if the puzzle does not contain any empty
    cell.
    """

    def test_invalid_search_algorithm_specified_exception_raised(self) -> None:
        puzzle = """
+-------+-------+-------+
| 6     |     4 |   8 5 |
| 9 7   |   6 5 |       |
|   4 8 | 7 3   |       |
+-------+-------+-------+
|   8   | 2 4 7 |       |
|     6 |   8   | 5     |
|       | 1 5 6 |   4   |
+-------+-------+-------+
|       |   1 3 | 2 6   |
|       | 6 9   |   3 4 |
| 2 6   | 4     |     9 |
+-------+-------+-------+
"""
        with raises(NoSuchAlgorithmError):
            TestSearchEngine.find_solution(puzzle, "NO-SUCH-ALGORITHM")

    def test_invalid_puzzle_duplicate_value_in_a_validation_block_exception_raised(self) -> None:
        invalid_puzzle = """
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
|       |       |       |
| 1   7 |   2   | 7   4 |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|       |       |       |
|       |       |       |
+-------+-------+-------+
"""
        with raises(InvalidPuzzleError):
            TestSearchEngine.find_solution(invalid_puzzle, "Smart-DFS")

    def test_puzzle_without_empty_cell_exception_raised(self) -> None:
        invalid_puzzle = """
+-------+-------+-------+
| 6 3 1 | 9 2 4 | 7 8 5 |
| 9 7 2 | 8 6 5 | 4 1 3 |
| 5 4 8 | 7 3 1 | 9 2 6 |
+-------+-------+-------+
| 3 8 5 | 2 4 7 | 6 9 1 |
| 4 1 6 | 3 8 9 | 5 7 2 |
| 7 2 9 | 1 5 6 | 3 4 8 |
+-------+-------+-------+
| 8 9 4 | 5 1 3 | 2 6 7 |
| 1 5 7 | 6 9 2 | 8 3 4 |
| 2 6 3 | 4 7 8 | 1 5 9 |
+-------+-------+-------+
"""
        with raises(InvalidPuzzleError):
            TestSearchEngine.find_solution(invalid_puzzle, "Smart-BFS")

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

from sudoku.grid import Grid
from sudoku.grid import get_cell_address
from sudoku.io import render_as_text


_ = None


def _assert_are_equivalent(expected_output: str, actual_output: str) -> None:
    expected_output = expected_output.strip()
    actual_output = actual_output.strip()
    assert expected_output == actual_output


class TestGridTextRenderer:
    """
    Collection of unit tests exercising the sudoku.io.render_as_text function.
    """
    pass

    def test_empty_grid_is_formatted_properly(self) -> None:
        cell_values = [
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
        ]

        expected_output = """
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
|       |       |       |
+-------+-------+-------+"""

        grid = Grid(cell_values)

        actual_output = render_as_text(grid, use_color=False)

        _assert_are_equivalent(expected_output, actual_output)

    def test_incomplete_grid_is_formatted_properly(self) -> None:
        cell_values = [
            [6, _, _, _, _, 4, _, 8, 5],
            [9, 7, _, _, 6, 5, _, _, _],
            [_, 4, 8, 7, 3, _, _, _, _],
            [_, 8, _, 2, 4, 7, _, _, _],
            [_, _, 6, _, 8, _, 5, _, _],
            [_, _, _, 1, 5, 6, _, 4, _],
            [_, _, _, _, 1, 3, 2, 6, _],
            [_, _, _, 6, 9, _, _, 3, 4],
            [2, 6, _, 4, _, _, _, _, 9],
        ]

        expected_output = """
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
+-------+-------+-------+"""

        grid = Grid(cell_values)

        actual_output = render_as_text(grid, use_color=False)

        _assert_are_equivalent(expected_output, actual_output)

    def test_complete_grid_is_formatted_properly(self) -> None:
        cell_values = [
            [_, 3, 1, 9, 2, 4, 7, 8, 5],
            [9, 7, 2, 8, 6, 5, 4, 1, 3],
            [5, 4, 8, 7, 3, 1, 9, 2, 6],
            [3, 8, 5, 2, 4, 7, 6, 9, 1],
            [4, 1, 6, 3, 8, _, 5, 7, 2],
            [7, 2, 9, 1, 5, 6, 3, 4, 8],
            [8, 9, 4, 5, 1, 3, 2, 6, 7],
            [1, 5, 7, 6, 9, 2, 8, 3, 4],
            [2, 6, 3, 4, 7, 8, 1, 5, 9],
        ]

        expected_output = """
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

        grid = Grid(cell_values)
        grid.set_cell_value(get_cell_address(0, 0), 6)
        grid.set_cell_value(get_cell_address(4, 5), 9)

        actual_output = render_as_text(grid, use_color=False)

        _assert_are_equivalent(expected_output, actual_output)

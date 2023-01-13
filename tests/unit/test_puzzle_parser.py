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

from sudoku.io import InvalidInputError
from sudoku.io.puzzle_parser import read_from_string


_ = None


class TestPuzzleParser:
    """
    Collection of unit tests exercising the sudoku.io.puzzle_parser module.
    """

    def test_parsing_of_valid_input_returns_proper_cell_values(self) -> None:
        valid_input = """
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
        expected_cell_values = [
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

        actual_cell_values = read_from_string(valid_input)
        assert actual_cell_values == expected_cell_values

    def test_parsing_of_valid_input_with_leading_and_trailing_whitespace_returns_proper_cell_values(self) -> None:
        valid_input = """
            +-------+-------+-------+
            | 3     |     4 |   9   |   
            | 1     |   6 5 |       |
            |     7 |   2   |       |
            +-------+-------+-------+   
            |   8   |   1 3 |       |
            |     6 |   8   | 5     |
            |       | 5   6 |   4   |
            +-------+-------+-------+
            |       |   1   | 4 6   |
            |       | 6 9   |   2   |
            | 2 7   | 4     |     9 |
            +-------+-------+-------+"""  # noqa: W291
        expected_cell_values = [
            [3, _, _, _, _, 4, _, 9, _],
            [1, _, _, _, 6, 5, _, _, _],
            [_, _, 7, _, 2, _, _, _, _],
            [_, 8, _, _, 1, 3, _, _, _],
            [_, _, 6, _, 8, _, 5, _, _],
            [_, _, _, 5, _, 6, _, 4, _],
            [_, _, _, _, 1, _, 4, 6, _],
            [_, _, _, 6, 9, _, _, 2, _],
            [2, 7, _, 4, _, _, _, _, 9],
        ]

        actual_cell_values = read_from_string(valid_input)
        assert actual_cell_values == expected_cell_values

    def test_letter_as_cell_value_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 6     |     4 |   8 5 |
| 9 7   |   6 5 |       |
|   4 8 | 7 x   |       |
+-------+-------+-------+
|   8   | 2 4 7 |       |
|     6 |   8   | 5     |
|       | 1 5 6 |   4   |
+-------+-------+-------+
|       |   1 3 | 2 6   |
|       | 6 9   |   3 4 |
| 2 6   | 4     |     9 |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Invalid cell value 'x'" in e.message
            assert "found in row 3" in e.message

    def test_special_character_as_cell_value_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 3     |       |   8 5 |
|   9   |   6 1 |       |
|   8 4 |       |       |
+-------+-------+-------+
|   4   | 2     |       |
|     6 |       | 5     |
|       | 1     |   4   |
+-------+-------+-------+
|     $ |   1   | 6     |
|       | 6     |   3   |
| 2 6   | 4     |     1 |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Invalid cell value '$'" in e.message
            assert "found in row 7" in e.message

    def test_zero_as_cell_value_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 1     |       |       |
|   5   |     9 |       |
|       |       | 2     |
+-------+-------+-------+
|   0   |       |       |
|       |       |   1   |
|       |   7   |       |
+-------+-------+-------+
|       |       | 6   4 |
|       |       | 8     |
|     4 |       |     3 |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Invalid cell value '0'" in e.message
            assert "found in row 4" in e.message

    def test_crippled_border_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 1     |       |       |
|   5   |     9 |       |
|       |       | 2     |
+-------+--
|   1   |       |       |
|       |       |   1   |
| 3     |   7   |       |
+-------+-------+-------+
|       |       | 6   4 |
|       |       | 8     |
|     4 |       |     3 |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Row 5 is not a valid border line." == e.message

    def test_invalid_character_in_border_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 1     |       |       |
|   5   |     9 |       |
|       |       | 2     |
+-------+-------+-------+
|   1   |       |       |
|       |       |   1   |
| 3     |   7   |       |
+---^---+-------+-------+
|       |       | 6   4 |
|       |       | 8     |
|     4 |       |     3 |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Row 9 is not a valid border line." == e.message

    def test_grid_with_missing_lines_leads_to_exception(self) -> None:
        invalid_input = """
+-------+-------+-------+
| 1     |       |       |
|   5   |     9 |       |
|       |       | 2     |
+-------+-------+-------+
|   1   |       |       |
|       |       |   1   |
| 3     |   7   |       |
+-------+-------+-------+"""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Row 10 is missing." == e.message

    def test_empty_input_leads_to_exception(self) -> None:
        invalid_input = ""
        with raises(InvalidInputError) as e:
            read_from_string(invalid_input)
            assert "Row 1 is missing." == e.message

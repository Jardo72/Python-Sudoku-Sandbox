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

from io import StringIO, TextIOWrapper
from typing import List

from .invalid_input_error import InvalidInputError


class _PuzzleParser:
    """
    Simple parser allowing to read and parse a textual representation of a puzzle
    from an input file or from a string. This class is internal - it is not supposed
    to be used directly by other modules.
    """

    _BORDER_LINE_TEMPLATE = "+-------+-------+-------+"

    _CELL_LINE_TEMPLATE = "| ? ? ? | ? ? ? | ? ? ? |"

    def __init__(self, input: StringIO | TextIOWrapper) -> None:
        self._lines = [line.strip() for line in input.readlines()]

    def _parse_border_line(self, index: int) -> None:
        if index >= len(self._lines):
            raise InvalidInputError(f"Row {index + 1} is missing.")
        if self._lines[index] != self._BORDER_LINE_TEMPLATE:
            raise InvalidInputError(f"Row {index + 1} is not a valid border line.")

    def _parse_cell_line(self, row_index: int) -> List[int | None]:
        result = []
        if row_index >= len(self._lines):
            raise InvalidInputError("Row {0} is missing.".format(row_index + 1))
        if (len(self._lines[row_index])) != len(self._CELL_LINE_TEMPLATE):
            raise InvalidInputError("Row {0} is not a valid cell line.".format(row_index + 1))
        for char_index in range(0, len(self._CELL_LINE_TEMPLATE)):
            if self._CELL_LINE_TEMPLATE[char_index] == '?':
                cell_value = self._parse_and_validate_cell_value(row_index, char_index)
                result.append(cell_value)
            elif self._CELL_LINE_TEMPLATE[char_index] != self._lines[row_index][char_index]:
                raise InvalidInputError("Row {0} is not a valid cell line.".format(row_index + 1))
        return result

    def _parse_and_validate_cell_value(self, row_index: int, char_index: int) -> int | None:
        if self._lines[row_index][char_index] not in " 123456789":
            raise InvalidInputError("Invalid cell value '{0}' found in row {1}.".format(self._lines[row_index][char_index], row_index + 1))
        if self._lines[row_index][char_index] == ' ':
            return None
        return int(self._lines[row_index][char_index])

    def get_cells(self) -> List[List[int | None]]:
        result = []
        for index in range(13):
            if index in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
                cell_values = self._parse_cell_line(index)
                result.append(cell_values)
            if index in [0, 4, 8, 12]:
                self._parse_border_line(index)
        return result


def read_from_file(filename: str) -> List[List[int | None]]:
    """
    Reads the input file with the given filename and parses the textual representation
    of the grid contained in it.

    Parameters:
        filename (str):    The name of the input file to be read and parsed.

    Returns:         List of lists, where a single value in such a nested list
                        corresponds to a single cell from the parsed grid. The None value
                        is used for undefined cells, int values between 1 and 9 are used
                        for defined cells.

    Raises:
        InvalidInputError   If the given input is invalid (e.g. crippled grid, invalid
                            cell values etc.).
    """
    with open(filename, "r") as file:
        parser = _PuzzleParser(file)
        return parser.get_cells()


def read_from_string(grid_as_string: str) -> List[List[int | None]]:
    """
    Reads and parses the given textual representation of a grid.

    Parameters:
        grid_as_string (str):    The textual representation of puzzle to be parsed.

    Returns:         List of lists, where a single value in such a nested list
                        corresponds to a single cell from the parsed grid. The None value
                        is used for undefined cells, int values between 1 and 9 are used
                        for defined cells.

    Raises:
        InvalidInputError   If the given input is invalid (e.g. crippled grid, invalid
                            cell values etc.).
    """
    with StringIO(grid_as_string.strip()) as input:
        parser = _PuzzleParser(input)
        return parser.get_cells()

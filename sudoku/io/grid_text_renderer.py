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

from io import StringIO

from colorama import Back, Fore

from sudoku.grid import CellStatus, Grid
from sudoku.grid import get_cell_address


def render_as_text(grid: Grid, use_color: bool = True) -> str:
    """
    Generates and returns textual representation of the given grid.

    Paramaters:
            grid (sudoku.grid.Grid):    The grid to be rendered.
            use_colors (bool):          True if ANSI escape sequences are to be used to highlight
                                        predefined cells (and thus distinguish them from the
                                        completed cells); False otherwise.

    Returns:
        str: The generated textual representation of the given grid.
    """
    renderer = _GridTextRenderer(grid, use_color)
    return renderer.render()


class _GridTextRenderer:
    """
    Simple renderer that can take an instance of the sudoku.grid.Grid class and
    generate a textual grid presenting the cell values of the given grid. Optionally,
    ANSI escape sequences can be used to highlight predefined cells.
    """

    _BORDER_LINE_TEMPLATE = "+-------+-------+-------+"

    _CELL_LINE_TEMPLATE = "| ? ? ? | ? ? ? | ? ? ? |"

    _GRID_BACKGROUND = Back.BLACK

    _GRID_FOREGROUND = Fore.WHITE

    _PREDEFINED_CELL_FOREGROUND = Fore.RED

    def __init__(self, grid: Grid, use_colors: bool = False) -> None:
        self._grid = grid
        self._use_colors = use_colors
        self._output = StringIO()

    def render(self) -> str:
        if self._use_colors:
            self._output.write("\n" + self._GRID_FOREGROUND + self._GRID_BACKGROUND)
        self._write_border()

        for range_of_rows in range(0, 3), range(3, 6), range(6, 9):
            for row in range_of_rows:
                self._write_cells(row)
            self._write_border()

        if self._use_colors:
            self._output.write("\n" + Fore.RESET + Back.RESET)
        return self._output.getvalue()

    def _write_border(self) -> None:
        if self._use_colors:
            self._output.write(self._GRID_FOREGROUND + self._GRID_BACKGROUND)
        self._output.write(self._BORDER_LINE_TEMPLATE)
        if self._use_colors:
            self._output.write(Fore.RESET + Back.RESET)
        self._output.write("\n")

    def _write_cells(self, row: int) -> None:
        output = self._CELL_LINE_TEMPLATE
        for column in range(9):
            cell_address = get_cell_address(row, column)
            cell_value = " "
            if self._grid.get_cell_status(cell_address) != CellStatus.UNDEFINED:
                cell_value = str(self._grid.get_cell_value(cell_address))
            if self._use_colors and self._grid.get_cell_status(cell_address) == CellStatus.PREDEFINED:
                cell_value = self._decorate_with_color(cell_value)
            output = output.replace("?", cell_value, 1)
        if self._use_colors:
            self._output.write(self._GRID_FOREGROUND + self._GRID_BACKGROUND)
        self._output.write(output)
        if self._use_colors:
            self._output.write(Fore.RESET + Back.RESET)
        self._output.write("\n")

    def _decorate_with_color(self, cell_value: str) -> str:
        return self._GRID_BACKGROUND + self._PREDEFINED_CELL_FOREGROUND + cell_value + self._GRID_BACKGROUND + self._GRID_FOREGROUND

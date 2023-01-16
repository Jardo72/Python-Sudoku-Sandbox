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

from importlib.resources import as_file, files

from jinja2 import Environment, BaseLoader

from sudoku.grid import CellStatus
from sudoku.grid import get_cell_address
from sudoku.search.engine import SearchSummary


def _load_template() -> str:
    template_resource = files("sudoku.io").joinpath("html-template.j2")
    with as_file(template_resource) as template_file:
        return template_file.read_text()


def render_as_html(search_summary: SearchSummary) -> str:
    """
    Generates and returns HTML representation of the given grid.

    Paramaters:
            grid (sudoku.grid.Grid):    The grid to be rendered.

    Returns:
        str: The generated HTML representation of the given grid.
    """
    renderer = _GridHtmlRenderer(search_summary)
    return renderer.render()


class _GridHtmlRenderer:
    """
    Simple renderer that can take an instance of the sudoku.grid.Grid class and
    generate an HTML grid presenting the cell values of the given grid.
    """

    def __init__(self, search_summary: SearchSummary) -> None:
        self._search_summary = search_summary
        self._environment = Environment(loader=BaseLoader())

    def render(self) -> str:
        values = [["" for column in range(9)] for row in range(9)]
        styles = [["" for column in range(9)] for row in range(9)]
        grid = self._search_summary.final_grid
        for row in range(9):
            for column in range(9):
                cell_address = get_cell_address(row, column)
                cell_status = grid.get_cell_status(cell_address)
                styles[row][column] = "cell"
                if cell_status == CellStatus.COMPLETED:
                    values[row][column] = str(grid.get_cell_value(cell_address))
                elif cell_status == CellStatus.PREDEFINED:
                    values[row][column] = str(grid.get_cell_value(cell_address))
                    styles[row][column] = "cell predefinedCell"
                else:
                    values[row][column] = ""

        template = self._environment.from_string(_load_template())
        return template.render(
            summary=self._search_summary,
            values=values,
            styles=styles,
            trim_blocks=True,
            lstrip_blocks=True
        )

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

from jinja2 import Environment, BaseLoader

from sudoku.grid import CellStatus, Grid
from sudoku.grid import get_cell_address


_TEMPLATE = """
<html>

<head>
<title>Search Summary</title>
<style>
body {
    background-color: #DDDDFF;
    padding: 30px;
}

table.gridLayout {
    border: 2px solid black;
    border-collapse: collapse;
}

td.region {
    border-style: none;
    text-align: center;
    vertical-align: center;
    padding: 0px
}

table.region {
    border-style: none;
    border-collapse: collapse;
    padding: 0px
}

td.cell {
    border: 2px solid black;
    border-collapse: collapse;

    width: 50px;
    height: 50px;
    text-align: center;
    vertical-align: center;
}

td.predefinedCell {
    font-weight: bold;
    font-size: 120%;
}
</style>
</head>

<body>
<table class='gridLayout'>
{% for region_row in [0, 1, 2] %}
<tr>
{% for region_column in [0, 1, 2] %}
<td class="region">
<table class='region'>
{% for row_within_region in [0, 1, 2] %}
<tr>
{% for column_within_region in [0, 1, 2] %}
<td class='{{ styles[region_row * 3 + row_within_region][region_column * 3 + column_within_region]}}'>{{ values[region_row * 3 + row_within_region][region_column * 3 + column_within_region] }}</td>
{% endfor %}
</tr>
{% endfor %}
</table>
</td>
{% endfor %}
</tr>
{% endfor %}
</table>
</body>
</html>
"""  # noqa: E501


def render_as_html(grid: Grid) -> str:
    """
    Generates and returns HTML representation of the given grid.

    Paramaters:
            grid (sudoku.grid.Grid):    The grid to be rendered.

    Returns:
        str: The generated HTML representation of the given grid.
    """
    renderer = _GridHtmlRenderer(grid)
    return renderer.render()


class _GridHtmlRenderer:
    """
    Simple renderer that can take an instance of the sudoku.grid.Grid class and
    generate an HTML grid presenting the cell values of the given grid.
    """

    def __init__(self, grid: Grid) -> None:
        self._grid = grid
        self._environment = Environment(loader=BaseLoader())

    def render(self) -> str:
        values = [["" for column in range(9)] for row in range(9)]
        styles = [["" for column in range(9)] for row in range(9)]
        for row in range(9):
            for column in range(9):
                cell_address = get_cell_address(row, column)
                cell_status = self._grid.get_cell_status(cell_address)
                styles[row][column] = "cell"
                if cell_status == CellStatus.COMPLETED:
                    values[row][column] = str(self._grid.get_cell_value(cell_address))
                elif cell_status == CellStatus.PREDEFINED:
                    values[row][column] = str(self._grid.get_cell_value(cell_address))
                    styles[row][column] = "cell predefinedCell"
                else:
                    values[row][column] = ""
        template = self._environment.from_string(_TEMPLATE)
        return template.render(values=values, styles=styles, trim_blocks=True, lstrip_blocks=True)

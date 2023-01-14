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
from sudoku.search.engine import SearchSummary


_TEMPLATE = """
<html>

<head>
<title>Search Summary</title>
<style>
body {
    background-color: #AFCEEB;
    padding: 30px;
}

h1 {
    font-weight: bold;
    font-size: 140%;
    padding-top: 10px;
}

table.summary {
    border: 2px solid black;
    border-collapse: collapse;
}

td.summary {
    border: 1px solid black;
    vertical-align: center;
    padding: 3px 6px;
}

table.gridLayout {
    border: 2px solid black;
    border-collapse: collapse;
}

td.region {
    border-style: none;
    text-align: center;
    vertical-align: center;
    padding: 0px;
}

table.region {
    border-style: none;
    border-collapse: collapse;
    padding: 0px;
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
<h1>Summary</h1>
<table class="summary">
<tr>
<td class="summary">Number of undefined cells in the puzzle</td>
<td class="summary">{{ summary.original_undefined_cell_count }}</td>
</tr>
<tr>
<td class="summary">Search algorithm</td>
<td class="summary">{{ summary.algorithm }}</td>
</tr>
<tr>
<td class="summary">Search outcome</td>
<td class="summary">{{ summary.outcome }}</td>
</tr>
<tr>
<td class="summary">Search duration [ms]</td>
<td class="summary">{{ summary.duration_millis }}</td>
</tr>
<tr>
<td class="summary">Number of tried cell values</td>
<td class="summary">{{ summary.cell_values_tried }}</td>
</tr>
</table>

<h1>Final Grid</h1>
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
        template = self._environment.from_string(_TEMPLATE)
        return template.render(
            summary=self._search_summary,
            values=values,
            styles=styles,
            trim_blocks=True,
            lstrip_blocks=True
        )

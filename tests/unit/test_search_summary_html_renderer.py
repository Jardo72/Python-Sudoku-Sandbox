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

from bs4 import BeautifulSoup

from sudoku.grid import Grid
from sudoku.grid import get_cell_address
from sudoku.io import render_as_html
from sudoku.search.engine import SearchOutcome, SearchSummary


class TestSearchSummaryHtmlRenderer:
    """
    Collection of unit tests exercising the sudoku.io.render_as_html function.
    """

    def _create_grid(self) -> Grid:
        _ = None
        initial_cell_values = [
            [1, _, _, _, _, _, _, _, 2],
            [_, _, _, _, 8, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, _, _, 5, _, _, _, _, _],
            [_, _, _, _, 6, _, _, _, _],
            [_, _, _, _, _, 7, _, _, _],
            [_, _, _, 9, _, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [3, _, _, _, _, _, _, _, 4],
        ]
        grid = Grid(initial_cell_values)

        grid.set_cell_value(get_cell_address(0, 2), 4)
        grid.set_cell_value(get_cell_address(6, 7), 1)
        grid.set_cell_value(get_cell_address(3, 5), 2)

        return grid

    def _create_summary(self) -> SearchSummary:
        return SearchSummary(
            algorithm="Basic-UCS",
            outcome=SearchOutcome.ALGORITHM_DEAD_END,
            final_grid=self._create_grid(),
            original_undefined_cell_count=72,
            duration_millis=8,
            cell_values_tried=3
        )

    def test_that_summary_is_rednered_properly(self) -> None:
        html = render_as_html(self._create_summary())
        soup = BeautifulSoup(html, "html.parser")

        element = soup.find(id="originalUndefinedCellCount")
        assert element.text == "72"

        element = soup.find(id="algorithm")
        assert element.text == "Basic-UCS"

        element = soup.find(id="outcome")
        assert element.text == str(SearchOutcome.ALGORITHM_DEAD_END)

        element = soup.find(id="durationMillis")
        assert element.text == "8"

        element = soup.find(id="cellValuesTried")
        assert element.text == "3"

    def test_that_undefined_cells_of_final_grid_are_rendered_properly(self) -> None:
        html = render_as_html(self._create_summary())
        soup = BeautifulSoup(html, "html.parser")

        cells_not_to_be_verified = [
            # predefined cells
            (0, 0),
            (0, 8),
            (1, 4),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 3),
            (8, 0),
            (8, 8),
            # completed cells
            (0, 2),
            (6, 7),
            (3, 5),
        ]
        for coordinates in [(row, column) for row in range(9) for column in range(9)]:
            if coordinates in cells_not_to_be_verified:
                continue
            row, column = coordinates
            element = soup.find(id=f"cell-{row}-{column}")
            css_class = element["class"]
            assert element.text.strip() == ""
            assert css_class == ["cell"]

    def test_that_predefined_cells_of_final_grid_are_rendered_properly(self) -> None:
        html = render_as_html(self._create_summary())
        soup = BeautifulSoup(html, "html.parser")

        cells_to_be_verified = [
            (0, 0, 1),
            (0, 8, 2),
            (1, 4, 8),
            (3, 3, 5),
            (4, 4, 6),
            (5, 5, 7),
            (6, 3, 9),
            (8, 0, 3),
            (8, 8, 4),
        ]
        for row, column, value in cells_to_be_verified:
            element = soup.find(id=f"cell-{row}-{column}")
            css_class = element["class"]
            assert element.text.strip() == str(value)
            assert css_class == ["cell", "predefinedCell"]

    def test_that_completed_cells_of_final_grid_are_rendered_properly(self) -> None:
        html = render_as_html(self._create_summary())
        soup = BeautifulSoup(html, "html.parser")

        cells_to_be_verified = [
            (0, 2, 4),
            (6, 7, 1),
            (3, 5, 2),
        ]
        for row, column, value in cells_to_be_verified:
            element = soup.find(id=f"cell-{row}-{column}")
            css_class = element["class"]
            assert element.text.strip() == str(value)
            assert css_class == ["cell"]

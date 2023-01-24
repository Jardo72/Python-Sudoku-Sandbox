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

from dataclasses import dataclass

from sudoku.io import read_from_string, render_as_text
from sudoku.search.engine import SearchSummary
from sudoku.search.engine import discover_search_algorithms, find_solution


@dataclass(frozen=True)
class TestSummary:
    search_summary: SearchSummary
    final_grid: str


class TestSearchEngine:

    @staticmethod
    def find_solution(puzzle: str, algorithm_name: str, timeout_sec: int = 10) -> TestSummary:
        initial_cell_values = read_from_string(puzzle)
        search_summary = find_solution(initial_cell_values, algorithm_name, timeout_sec)
        final_grid = render_as_text(search_summary.final_grid, use_color=False)
        return TestSummary(search_summary, final_grid)


def _assert_are_equivalent(expected_output: str, actual_output: str) -> None:
    expected_output = expected_output.strip()
    actual_output = actual_output.strip()
    assert expected_output == actual_output


discover_search_algorithms()

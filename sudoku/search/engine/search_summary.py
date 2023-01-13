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

from .search_outcome import SearchOutcome
from sudoku.grid import Grid


@dataclass(frozen=True)
class SearchSummary:
    """
    Immutable structure carrying detailed information about the outcome of a search
    including the solution (or final grid in case the search has led to a dead end).
    """
    algorithm: str
    outcome: SearchOutcome
    final_grid: Grid
    original_undefined_cell_count: int
    duration_millis: int
    cell_values_tried: int

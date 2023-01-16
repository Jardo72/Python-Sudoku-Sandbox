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

from logging import getLogger

from sudoku.grid import Grid
from sudoku.search.engine import AbstractSearchAlgorithm, SearchStepOutcome
from sudoku.search.engine import search_algorithm
from sudoku.search.util import SearchSupport


_logger = getLogger(__name__)


@search_algorithm("UCS")
class UnambiguousCandidateSearch(AbstractSearchAlgorithm):

    def initialize(self, puzzle: Grid) -> None:
        _logger.info("Starting the search")
        self._search_support = SearchSupport(grid=puzzle)

    def apply_cell_value(self) -> SearchStepOutcome:
        _logger.info("Starting the next search step")
        candidate = self._search_support.get_unambiguous_candidate()
        if candidate is None:
            _logger.info("No applicable candidate found in queue, going to abort the search")
            if self._search_support.has_empty_cells_without_applicable_candidates():
                return SearchStepOutcome.PUZZLE_DEAD_END
            else:
                return SearchStepOutcome.ALGORITHM_DEAD_END

        self._search_support.set_cell_value(candidate.cell_address, candidate.value)

        if self._search_support.has_completed_grid():
            _logger.info("Search completed, solution found")
            return SearchStepOutcome.SOLUTION_FOUND

        return SearchStepOutcome.CONTINUE

    def get_grid_snapshot(self) -> Grid:
        return self._search_support.get_grid_snapshot()

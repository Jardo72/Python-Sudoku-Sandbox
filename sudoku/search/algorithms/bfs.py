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

from collections import deque
from dataclasses import dataclass
from logging import getLogger
from typing import Deque

from sudoku.grid import CellAddress, Grid
from sudoku.search.engine import AbstractSearchAlgorithm, SearchStepOutcome
from sudoku.search.engine import search_algorithm
from sudoku.search.util import CandidateQueryMode, SearchSupport


_logger = getLogger(__name__)


@dataclass(frozen=True, slots=True)
class _StepInput:
    """
    Internal structure supporting the implementation of the BFS algorithm. Single
    instance of this class represents a single entry in the queue used by the BFS
    algorithm.
    """
    search_support: SearchSupport
    cell_address: CellAddress
    value: int


class _BreadthFirstSearch(AbstractSearchAlgorithm):
    """
    Base class providing functionality common to both breadth-first search (BFS)
    implementations of search algorithm.
    """

    __slots__ = "_candidate_query_mode", "_queue"

    def __init__(self, candidate_query_mode: CandidateQueryMode) -> None:
        self._candidate_query_mode = candidate_query_mode
        self._queue: Deque = deque()

    def initialize(self, puzzle: Grid) -> None:
        _logger.info("Starting the search")
        self._grid_snapshot = puzzle.copy()
        self._enqueue_steps(SearchSupport(puzzle.copy()))

    def apply_cell_value(self) -> SearchStepOutcome:
        _logger.info("Starting the next search step")
        return self._process_next_step_from_queue()

    def get_grid_snapshot(self) -> Grid:
        return self._grid_snapshot

    def _enqueue_steps(self, search_support: SearchSupport) -> None:
        if search_support.has_empty_cells_without_applicable_candidates():
            _logger.info("Empty cells without applicable candidates found, nothing will be added to queue")
            return
        candidate_list = search_support.get_undefined_cell_candidates(self._candidate_query_mode)
        assert len(candidate_list) > 0  # type: ignore
        for single_value in candidate_list.values:  # type: ignore
            self._queue.append(_StepInput(search_support.copy(), candidate_list.cell_address, single_value))  # type: ignore

    def _process_next_step_from_queue(self) -> SearchStepOutcome:
        if len(self._queue) == 0:
            _logger.info("Empty queue, going to abort the search")
            return SearchStepOutcome.PUZZLE_DEAD_END

        step_input = self._queue.popleft()
        search_support = step_input.search_support

        search_support.set_cell_value(step_input.cell_address, step_input.value)
        self._grid_snapshot = search_support.get_grid_snapshot()
        if search_support.has_completed_grid():
            _logger.info("Search completed, solution found")
            return SearchStepOutcome.SOLUTION_FOUND

        self._enqueue_steps(search_support.copy())
        return SearchStepOutcome.CONTINUE


@search_algorithm("Naive-BFS")
class NaiveBreadthFirstSearch(_BreadthFirstSearch):
    """
    Naive implementation of the BFS search algorithm.
    """

    def __init__(self) -> None:
        super().__init__(CandidateQueryMode.FIRST_UNDEFINED_CELL)


@search_algorithm("Smart-BFS")
class SmartBreadthFirstSearch(_BreadthFirstSearch):
    """
    Smart implementation of the BFS search algorithm.
    """

    def __init__(self) -> None:
        super().__init__(CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES)

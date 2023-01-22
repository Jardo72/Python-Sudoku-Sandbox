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

from __future__ import annotations
from logging import getLogger
from time import perf_counter
from typing import List, Optional

from sudoku.grid import Grid
from .abstract_search_algorithm import AbstractSearchAlgorithm
from .invalid_puzzle_error import InvalidPuzzleError
from .search_algorithm_registry import SearchAlgorithmRegistry
from .search_outcome import SearchOutcome
from .search_step_outcome import SearchStepOutcome
from .search_summary import SearchSummary


_logger = getLogger(__name__)


class _OutcomeMapping:

    _entries = {
        SearchStepOutcome.SOLUTION_FOUND: SearchOutcome.SOLUTION_FOUND,
        SearchStepOutcome.ALGORITHM_DEAD_END: SearchOutcome.ALGORITHM_DEAD_END,
        SearchStepOutcome.PUZZLE_DEAD_END: SearchOutcome.PUZZLE_DEAD_END
    }

    @staticmethod
    def convert(step_outcome: SearchStepOutcome) -> SearchOutcome:
        assert step_outcome in _OutcomeMapping._entries
        return _OutcomeMapping._entries[step_outcome]


class _Stopwatch:
    """
    Simple stopwatch used to measure the duration of a search. This class is not supposed to be
    directly instantiated by other classes. Instead, the static start() method is to be used.
    """

    def __init__(self) -> None:
        self._start_time = perf_counter()

    @staticmethod
    def start() -> _Stopwatch:
        return _Stopwatch()

    def elapsed_time_millis(self) -> int:
        duration = perf_counter() - self._start_time
        return int(1000 * duration)

    def elapsed_time_seconds(self) -> float:
        return perf_counter() - self._start_time


class _SearchJob:
    """
    Internal helper class supporting the implementation of the search engine. Single instance of
    this class drives a single search by invoking the search algorithm and evaluating the search
    step outcome.
    """

    def __init__(self, puzzle: Grid, search_algorithm: AbstractSearchAlgorithm, timeout_sec: int) -> None:
        self._puzzle = puzzle
        self._search_algorithm = search_algorithm
        self._timeout_sec = timeout_sec
        self._last_step_outcome = SearchStepOutcome.CONTINUE
        self._duration_millis = 0
        self._cell_values_tried = 0

    def execute(self) -> None:
        stopwatch = _Stopwatch.start()
        try:
            self._search_algorithm.initialize(self._puzzle)
            step_outcome = self._search_algorithm.apply_cell_value()
            self._update_search_state(step_outcome)
            _logger.info("Very first search step completed, outcome = %s", step_outcome)
            while step_outcome == SearchStepOutcome.CONTINUE:
                if self._timeout_sec < stopwatch.elapsed_time_seconds():
                    _logger.error("Search not completed yet, timeout already reached")
                    message = f"Timeout {self._timeout_sec} sec expired ({self._cell_values_tried} cell values tried)."
                    raise TimeoutError(message)
                step_outcome = self._search_algorithm.apply_cell_value()
                self._update_search_state(step_outcome)
                _logger.info("Another search step completed, outcome = %s", step_outcome)
        finally:
            self._duration_millis = stopwatch.elapsed_time_millis()

    def _update_search_state(self, step_outcome: SearchStepOutcome) -> None:
        self._last_step_outcome = step_outcome
        if step_outcome in [SearchStepOutcome.CONTINUE, SearchStepOutcome.SOLUTION_FOUND]:
            self._cell_values_tried += 1
        _logger.debug("Last step outcome = %s, %d cell values tried", self._last_step_outcome, self._cell_values_tried)

    @property
    def last_step_outcome(self) -> SearchStepOutcome:
        return self._last_step_outcome

    @property
    def final_grid(self) -> Grid:
        return self._search_algorithm.get_grid_snapshot()

    @property
    def cell_values_tried(self) -> int:
        return self._cell_values_tried

    @property
    def duration_millis(self) -> int:
        return self._duration_millis


def find_solution(puzzle_cell_values: List[List[Optional[int]]], algorithm_name: str, timeout_sec: int) -> SearchSummary:
    _logger.info("Going to start %s search (timeout = %d sec)", algorithm_name, timeout_sec)
    puzzle = Grid(puzzle_cell_values)
    if not puzzle.is_valid():
        _logger.error("Puzzle not valid")
        message = "The given puzzle violates the game rules. At least one value is present two or more " \
                  "times in a single row, single column, or single region."
        raise InvalidPuzzleError(message)
    if puzzle.is_complete():
        _logger.error("Puzzle already complete")
        raise InvalidPuzzleError("The given puzzle does not contain empty cells - there is nothing to be solved.")

    search_algorithm = SearchAlgorithmRegistry.create_algorithm_instance(algorithm_name)
    _logger.debug("Search algorithm instantiated")

    search_job = _SearchJob(puzzle.copy(), search_algorithm, timeout_sec)
    search_outcome = None

    try:
        search_job.execute()
        search_outcome = _OutcomeMapping.convert(search_job.last_step_outcome)
        if search_outcome == SearchOutcome.SOLUTION_FOUND:
            assert search_job.final_grid.is_valid()
    except TimeoutError:
        search_outcome = SearchOutcome.TIMEOUT

    return SearchSummary(
        algorithm=algorithm_name,
        outcome=search_outcome,
        final_grid=search_job.final_grid,
        original_undefined_cell_count=puzzle.undefined_cell_count,
        duration_millis=search_job.duration_millis,
        cell_values_tried=search_job.cell_values_tried
    )

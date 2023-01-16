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
from logging import getLogger
from typing import Deque

from sudoku.grid import CellAddress, Grid
from sudoku.search.engine import AbstractSearchAlgorithm, SearchStepOutcome
from sudoku.search.engine import search_algorithm
from sudoku.search.util import CandidateList, CandidateQueryMode, SearchSupport


_logger = getLogger(__name__)


class _SearchGraphNode:
    """
    Internal helper class supporting the implementation of the DFS algorithm. Single
    instance of this class represents a single entry in the stack used by the DFS
    algorithm.
    """

    def __init__(self, search_support: SearchSupport, candidate_list: CandidateList) -> None:
        self._search_support = search_support
        self._candidate_list = candidate_list
        self._current_index = 0
        assert len(candidate_list) > 0

    @property
    def search_support(self) -> SearchSupport:
        return self._search_support

    @property
    def cell_address(self) -> CellAddress:
        return self._candidate_list.cell_address

    @property
    def already_exhausted(self) -> bool:
        if self._candidate_list is None:
            return True
        return self._current_index >= len(self._candidate_list)

    def next_value(self) -> int:
        values = self._candidate_list.values
        result = values[self._current_index]
        self._current_index += 1
        return result


class _SearchGraphNodeStack:
    """
    Internal helper class supporting the implementation of the DFS algorithm. This class
    implements the stack used by the DFS algorithm.
    """

    def __init__(self) -> None:
        self._entries: Deque = deque()

    def push(self, node: _SearchGraphNode) -> None:
        self._entries.append(node)
        _logger.debug("Node pushed to stack: %s", node)

    def backtrack_to_first_unexhausted_node(self) -> _SearchGraphNode | None:
        node = self._peek()
        while node is not None and node.already_exhausted:
            self._pop()
            node = self._peek()
        _logger.debug("Backtracked to node %s", node)
        return node

    def _pop(self) -> _SearchGraphNode | None:
        if len(self._entries) == 0:
            return None
        return self._entries.pop()

    def _peek(self) -> _SearchGraphNode | None:
        if len(self._entries) == 0:
            return None
        return self._entries[-1]


class _DepthFirstSearch(AbstractSearchAlgorithm):
    """
    Base class providing functionality common to both depth-first search (DFS)
    implementations of search algorithm.
    """

    def __init__(self, candidate_query_mode: CandidateQueryMode) -> None:
        self._candidate_query_mode = candidate_query_mode
        self._stack = _SearchGraphNodeStack()

    def initialize(self, puzzle: Grid) -> None:
        _logger.info("Starting the search")
        self._grid_snapshot = puzzle.copy()
        search_support = SearchSupport(puzzle.copy())
        if search_support.has_empty_cells_without_applicable_candidates():
            _logger.info("Empty cells without applicable candidates found, nothing will be pushed to stack")
            return
        candidate_list = search_support.get_undefined_cell_candidates(self._candidate_query_mode)
        node = _SearchGraphNode(search_support, candidate_list)  # type: ignore
        self._stack.push(node)

    def apply_cell_value(self) -> SearchStepOutcome:
        node = self._stack.backtrack_to_first_unexhausted_node()
        if node is None:
            _logger.info("Unexhausted node not found in the stack, going to abort the search")
            return SearchStepOutcome.PUZZLE_DEAD_END

        search_support = node.search_support
        cell_address = node.cell_address
        value = node.next_value()

        search_support = search_support.copy()
        search_support.set_cell_value(cell_address, value)
        self._grid_snapshot = search_support.get_grid_snapshot()
        if search_support.has_completed_grid():
            _logger.info("Search completed, solution found")
            return SearchStepOutcome.SOLUTION_FOUND

        if not search_support.has_empty_cells_without_applicable_candidates():
            candidate_list = search_support.get_undefined_cell_candidates(self._candidate_query_mode)
            node = _SearchGraphNode(search_support, candidate_list)  # type: ignore
            self._stack.push(node)

        return SearchStepOutcome.CONTINUE

    def get_grid_snapshot(self) -> Grid:
        return self._grid_snapshot


@search_algorithm("Naive-DFS")
class NaiveDepthFirstSearch(_DepthFirstSearch):
    """
    Naive implementation of the DFS search algorithm.
    """

    def __init__(self) -> None:
        super().__init__(CandidateQueryMode.FIRST_UNDEFINED_CELL)


@search_algorithm("Smart-DFS")
class SmartDepthFirstSearch(_DepthFirstSearch):
    """
    Smart implementation of the DFS search algorithm.
    """

    def __init__(self) -> None:
        super().__init__(CandidateQueryMode.UNDEFINED_CELL_WITH_LEAST_CANDIDATES)

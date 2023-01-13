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

from abc import ABC, abstractmethod

from sudoku.grid import Grid
from .search_step_outcome import SearchStepOutcome


class AbstractSearchAlgorithm(ABC):
    """
    Abstract base class prescribing the interface the search algorithm implementations have
    to implement.
    """

    @abstractmethod
    def initialize(self, puzzle: Grid) -> None:
        """
        This method is automatically invoked by the search engine at the beginning of the search.
        Implementations of this method are supposed to perform an initialization of the search
        algorithm.

            Paramateres:
                puzzle (Grid):      Grid reprezenting the puzzle to be solved by this search algorithm
                                    instance.
        """
        ...

    @abstractmethod
    def apply_cell_value(self) -> SearchStepOutcome:
        """
        This method is repeatedly invoked by the search engine until the return value of this method
        indicates that the search is completed (regardless of whether the search has been successful).
        Single invocation of this method is supposed to apply a single cell value.

            Returns:
                SearchStepOutcome:      Value indicating whether the search has to continue or not. If the
                                        search has completed, the value allows to distinguish whether
                                        a solution has been found, or the algorithm has failed to find
                                        a solution.
        """
        ...

    @abstractmethod
    def get_grid_snapshot(self) -> Grid:
        """
        Creates and returns a new snapshot of the grid representing the status of the search after the
        last invocation of the apply_cell_value method.

            Returns:
                Grid:   The created snapshot. The returned grid is supposed to be a copy of the grid used
                        internally by this search algorithm, so eventual modification of the snapshot will
                        not impact the internal status of the search.
        """
        ...

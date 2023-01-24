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

from pytest import mark, raises

from sudoku.grid import Grid
from sudoku.search.engine import AbstractSearchAlgorithm, NoSuchAlgorithmError, SearchAlgorithmRegistry, SearchStepOutcome
from sudoku.search.engine import search_algorithm


@search_algorithm("test-alg-1")
class TestAlgorithmOne(AbstractSearchAlgorithm):

    def initialize(self, puzzle: Grid) -> None:
        ...

    def apply_cell_value(self) -> SearchStepOutcome:
        ...

    def get_grid_snapshot(self) -> Grid:
        ...

    @property
    def name(self) -> str:
        return "test-alg-1"


@search_algorithm("test-alg-2")
class TestAlgorithmTwo(AbstractSearchAlgorithm):

    def initialize(self, puzzle: Grid) -> None:
        ...

    def apply_cell_value(self) -> SearchStepOutcome:
        ...

    def get_grid_snapshot(self) -> Grid:
        ...

    @property
    def name(self) -> str:
        return "test-alg-2"


class TestSearchAlgorithmRegistry:
    """
    Collection of unit tests exercising the sudoku.search.engine.SearchAlgorithmRegistry class.
    """

    @mark.parametrize("name", ["test-alg-1", "test-alg-2"])
    def test_registered_algorithms_are_properly_instantiated(self, name: str) -> None:
        algorithm = SearchAlgorithmRegistry.create_algorithm_instance(name)
        assert algorithm.name == name

    def test_attempt_to_instantiate_unknown_algorithm_leads_to_exception(self) -> None:
        with raises(NoSuchAlgorithmError) as e:
            SearchAlgorithmRegistry.create_algorithm_instance("no-such-algorithm")
            assert "Unknown search algorithm no-such-algorithm" in e.message

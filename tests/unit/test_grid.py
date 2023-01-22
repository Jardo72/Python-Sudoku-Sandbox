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

from typing import Optional, Sequence, Tuple

from pytest import mark, raises

from sudoku.grid import CellAddress, CellStatus, Grid
from sudoku.grid import get_all_cell_addresses, get_cell_address
from sudoku.grid.grid import _CellSingletons


_ = None


def _completely_undefined_cell_values() -> Sequence[Sequence[int]]:
    return [[None for column in range(9)] for row in range(9)]


def _complete_and_valid_cell_values() -> Sequence[Sequence[int]]:
    return [
        [6, 3, 1, 9, 2, 4, 7, 8, 5],
        [9, 7, 2, 8, 6, 5, 4, 1, 3],
        [5, 4, 8, 7, 3, 1, 9, 2, 6],
        [3, 8, 5, 2, 4, 7, 6, 9, 1],
        [4, 1, 6, 3, 8, 9, 5, 7, 2],
        [7, 2, 9, 1, 5, 6, 3, 4, 8],
        [8, 9, 4, 5, 1, 3, 2, 6, 7],
        [1, 5, 7, 6, 9, 2, 8, 3, 4],
        [2, 6, 3, 4, 7, 8, 1, 5, 9],
    ]


class TestCellSingletons:

    def test_undefined_cell_is_singleton(self) -> None:
        ref_1 = _CellSingletons.get_undefined_cell()
        ref_2 = _CellSingletons.get_undefined_cell()
        ref_3 = _CellSingletons.get_undefined_cell()

        assert ref_1 is ref_2
        assert ref_1 is ref_3
        assert ref_2 is ref_3

    @mark.parametrize("value", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_there_is_singleton_cell_for_each_of_the_nine_predefined_values(self, value: int) -> None:
        ref_1 = _CellSingletons.get_predefined_cell(value)
        ref_2 = _CellSingletons.get_predefined_cell(value)
        ref_3 = _CellSingletons.get_predefined_cell(value)

        assert ref_1 is ref_2
        assert ref_1 is ref_3
        assert ref_2 is ref_3

    @mark.parametrize("value", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_there_is_singleton_cell_for_each_of_the_nine_completed_values(self, value: int) -> None:
        ref_1 = _CellSingletons.get_completed_cell(value)
        ref_2 = _CellSingletons.get_completed_cell(value)
        ref_3 = _CellSingletons.get_completed_cell(value)

        assert ref_1 is ref_2
        assert ref_1 is ref_3
        assert ref_2 is ref_3

    def test_undefined_cell_has_proper_status(self) -> None:
        cell = _CellSingletons.get_undefined_cell()

        assert cell.status == CellStatus.UNDEFINED

    def test_attempt_to_access_the_value_of_undefined_cell_leads_to_exception(self) -> None:
        cell = _CellSingletons.get_undefined_cell()

        with raises(AssertionError) as e:
            cell.value
            assert "does not have value" in e.message

    @mark.parametrize("value", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_predefined_cell_for_the_given_value_has_proper_value_and_status(self, value: int) -> None:
        cell = _CellSingletons.get_predefined_cell(value)

        assert cell.value == value
        assert cell.status == CellStatus.PREDEFINED

    @mark.parametrize("value", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_completed_cell_for_the_given_value_has_proper_value_and_status(self, value: int) -> None:
        cell = _CellSingletons.get_completed_cell(value)

        assert cell.value == value
        assert cell.status == CellStatus.COMPLETED


class TestValidity:

    def test_grid_with_two_equal_predefined_values_in_the_same_row_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[2][3] = initial_cell_values[2][7] = 5

        grid = Grid(initial_cell_values)

        assert not grid.is_valid()

    def test_grid_with_two_equal_completed_values_in_the_same_row_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(4, 2), 5)
        grid.set_cell_value(get_cell_address(4, 5), 5)

        assert not grid.is_valid()

    def test_grid_with_the_same_predefined_and_completed_value_in_the_same_row_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[7][1] = 2

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(7, 4), 2)

        assert not grid.is_valid()

    def test_grid_with_two_equal_predefined_values_in_the_same_column_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[3][2] = initial_cell_values[7][2] = 9

        grid = Grid(initial_cell_values)

        assert not grid.is_valid()

    def test_grid_with_two_equal_completed_values_in_the_same_column_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(2, 4), 6)
        grid.set_cell_value(get_cell_address(5, 4), 6)

        assert not grid.is_valid()

    def test_grid_with_the_same_predefined_and_completed_value_in_the_same_column_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[1][7] = 2

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(5, 7), 2)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_left_upper_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(0, 0), 9)
        grid.set_cell_value(get_cell_address(1, 2), 9)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_middle_upper_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(0, 4), 6)
        grid.set_cell_value(get_cell_address(2, 5), 6)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_right_upper_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[1][6] = 6

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(2, 7), 6)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_left_middle_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[3][0] = 8

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(4, 1), 8)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_central_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[4][3] = initial_cell_values[5][5] = 2

        grid = Grid(initial_cell_values)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_right_middle_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(3, 8), 1)
        grid.set_cell_value(get_cell_address(5, 7), 1)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_left_bottom_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[7][0] = 3

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(6, 2), 3)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_middle_bottom_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[7][3] = initial_cell_values[8][5] = 2

        grid = Grid(initial_cell_values)

        assert not grid.is_valid()

    def test_grid_with_two_equal_values_in_the_right_bottom_region_is_not_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(8, 8), 3)
        grid.set_cell_value(get_cell_address(6, 7), 3)

        assert not grid.is_valid()

    def test_incomplete_grid_without_violation_is_valid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[1][0] = 3
        initial_cell_values[4][6] = 1
        initial_cell_values[5][7] = 4
        initial_cell_values[8][3] = 7

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(2, 1), 6)
        grid.set_cell_value(get_cell_address(6, 4), 9)
        grid.set_cell_value(get_cell_address(7, 8), 2)

        assert grid.is_valid()

    def test_complete_grid_without_violation_is_valid(self) -> None:
        grid = Grid(_complete_and_valid_cell_values())

        assert grid.is_valid()


class TestCompletness:

    def test_grid_with_undefined_cells_only_is_not_complete(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)

        assert not grid.is_complete()

    def test_grid_with_mixture_of_undefined_cells_and_cells_with_value_is_not_complete(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[0][1] = initial_cell_values[5][4] = initial_cell_values[7][3] = 2
        initial_cell_values[4][3] = initial_cell_values[2][7] = initial_cell_values[6][4] = 5

        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(2, 6), 4)
        grid.set_cell_value(get_cell_address(8, 2), 7)
        grid.set_cell_value(get_cell_address(6, 8), 3)

        assert not grid.is_complete()

    def test_grid_with_all_cells_having_value_is_complete(self) -> None:
        initial_cell_values = _complete_and_valid_cell_values()

        grid = Grid(initial_cell_values)

        assert grid.is_complete()

    def test_even_invalid_grid_is_complete_if_each_cells_has_value(self) -> None:
        initial_cell_values = _complete_and_valid_cell_values()
        initial_cell_values[0][0] = initial_cell_values[0][1] = 6

        grid = Grid(initial_cell_values)

        assert grid.is_complete()


class TestUndefinedCellCount:

    def test_empty_grid_has_eighty_one_undefined_cells(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()

        grid = Grid(initial_cell_values)

        assert grid.undefined_cell_count == 81

    def test_proper_number_of_undefined_cells_is_provided_for_incomplete_grid(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[0][0] = 3
        initial_cell_values[1][7] = 8
        initial_cell_values[5][4] = 2

        grid = Grid(initial_cell_values)

        assert grid.undefined_cell_count == 78

    def test_complete_grid_has_zero_undefined_cells(self) -> None:
        initial_cell_values = _complete_and_valid_cell_values()

        grid = Grid(initial_cell_values)

        assert grid.undefined_cell_count == 0

    def test_undefined_cell_count_is_decreased_whenever_cell_is_completed(self) -> None:
        initial_cell_values = _completely_undefined_cell_values()
        initial_cell_values[0][0] = 7
        initial_cell_values[0][4] = 5
        initial_cell_values[1][2] = 3
        initial_cell_values[1][6] = 4
        initial_cell_values[3][4] = 9
        initial_cell_values[3][8] = 1
        initial_cell_values[7][5] = 2
        initial_cell_values[7][7] = 6

        grid = Grid(initial_cell_values)
        assert grid.undefined_cell_count == 73

        grid.set_cell_value(get_cell_address(0, 2), 3)
        assert grid.undefined_cell_count == 72

        grid.set_cell_value(get_cell_address(2, 5), 7)
        assert grid.undefined_cell_count == 71

        grid.set_cell_value(get_cell_address(8, 3), 4)
        assert grid.undefined_cell_count == 70


class TestCellManipulation:

    def test_undefined_cells_have_proper_value_and_status(self) -> None:
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

        verification_list = [
            get_cell_address(0, 1),
            get_cell_address(1, 0),
            get_cell_address(0, 7),
            get_cell_address(1, 8),
            get_cell_address(7, 0),
            get_cell_address(8, 1),
            get_cell_address(7, 8),
            get_cell_address(8, 7),
            get_cell_address(5, 3),
            get_cell_address(3, 6),
            get_cell_address(6, 5)
        ]
        for cell_address in verification_list:
            assert grid.get_cell_value(cell_address) is None
            assert grid.get_cell_status(cell_address) == CellStatus.UNDEFINED

    def test_predefined_cells_have_proper_value_and_status(self) -> None:
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

        verification_list = [
            (get_cell_address(0, 0), 1),
            (get_cell_address(0, 8), 2),
            (get_cell_address(8, 0), 3),
            (get_cell_address(8, 8), 4),
            (get_cell_address(1, 4), 8),
            (get_cell_address(3, 3), 5),
            (get_cell_address(4, 4), 6),
            (get_cell_address(5, 5), 7),
            (get_cell_address(6, 3), 9)
        ]
        for cell_address, value in verification_list:
            assert grid.get_cell_value(cell_address) == value
            assert grid.get_cell_status(cell_address) == CellStatus.PREDEFINED

    def test_completed_cells_have_proper_value_and_status(self) -> None:
        initial_cell_values = [
            [6, _, _, _, _, 4, _, 8, 5],
            [9, 7, _, _, 6, 5, _, _, _],
            [_, 4, 8, 7, 3, _, _, _, _],
            [_, 8, _, 2, 4, 7, _, _, _],
            [_, _, 6, _, 8, _, 5, _, _],
            [_, _, _, 1, 5, 6, _, 4, _],
            [_, _, _, _, 1, 3, 2, 6, _],
            [_, _, _, 6, 9, _, _, 3, 4],
            [2, 6, _, 4, _, _, _, _, 9],
        ]
        grid = Grid(initial_cell_values)

        modification_list = [
            (get_cell_address(0, 1), 3),
            (get_cell_address(2, 8), 1),
            (get_cell_address(5, 0), 7),
            (get_cell_address(3, 6), 3),
            (get_cell_address(8, 7), 5)
        ]
        for cell_address, value in modification_list:
            grid.set_cell_value(cell_address, value)
            assert grid.get_cell_value(cell_address) == value
            assert grid.get_cell_status(cell_address) == CellStatus.COMPLETED

    def test_modification_of_predefined_cell_leads_to_exception(self) -> None:
        initial_cell_values = [
            [4, 1, _, _, _, _, _, _, _],
            [7, _, _, _, _, _, _, _, _],
            [_, _, 4, _, _, _, _, _, _],
            [_, _, _, _, _, _, 3, _, _],
            [_, _, _, _, 9, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 8, _, _],
            [_, _, _, _, _, _, _, _, _],
        ]
        grid = Grid(initial_cell_values)

        modification_list = [
            (get_cell_address(0, 0), 2),
            (get_cell_address(0, 1), 3),
            (get_cell_address(4, 4), 8),
            (get_cell_address(3, 6), 9),
            (get_cell_address(7, 6), 5)
        ]
        for cell_address, value in modification_list:
            with raises(ValueError):
                grid.set_cell_value(cell_address, value)

    def test_modification_of_completed_cell_leads_to_exception(self) -> None:
        initial_cell_values = [
            [4, 1, _, _, _, _, _, _, _],
            [7, _, _, _, _, _, _, _, _],
            [_, _, 4, _, _, _, _, _, _],
            [_, _, _, _, _, _, 3, _, _],
            [_, _, _, _, 9, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 8, _, _],
            [_, _, _, _, _, _, _, _, _],
        ]
        grid = Grid(initial_cell_values)
        grid.set_cell_value(get_cell_address(1, 8), 2)

        with raises(ValueError):
            grid.set_cell_value(get_cell_address(1, 8), 3)


class TestCloning:

    def test_clone_has_the_same_cell_values_and_states_as_the_original_grid(self) -> None:
        initial_cell_values = [
            [6, _, _, _, _, 4, _, 8, 5],
            [9, 7, _, _, 6, 5, _, _, _],
            [_, 4, 8, 7, 3, _, _, _, _],
            [_, 8, _, 2, 4, 7, _, _, _],
            [_, _, 6, _, 8, _, 5, _, _],
            [_, _, _, 1, 5, 6, _, 4, _],
            [_, _, _, _, 1, 3, 2, 6, _],
            [_, _, _, 6, 9, _, _, 3, 4],
            [2, 6, _, 4, _, _, _, _, 9],
        ]
        original_grid = Grid(initial_cell_values)
        original_grid.set_cell_value(get_cell_address(0, 2), 1)
        original_grid.set_cell_value(get_cell_address(8, 7), 5)
        clone = original_grid.copy()

        for cell_address in get_all_cell_addresses():
            assert original_grid.get_cell_status(cell_address) == clone.get_cell_status(cell_address)
            assert original_grid.get_cell_value(cell_address) == clone.get_cell_value(cell_address)

    def test_modification_of_clone_does_not_change_original_grid(self) -> None:
        original_grid = Grid(self._initial_cell_values)
        clone = original_grid.copy()

        for cell_address, value in self._modification_list:
            clone.set_cell_value(cell_address, value)
            assert original_grid.get_cell_status(cell_address) == CellStatus.UNDEFINED
            assert original_grid.get_cell_value(cell_address) is None

    def test_modification_of_original_grid_does_not_change_clone(self) -> None:
        original_grid = Grid(self._initial_cell_values)
        clone = original_grid.copy()

        for cell_address, value in self._modification_list:
            original_grid.set_cell_value(cell_address, value)
            assert clone.get_cell_status(cell_address) == CellStatus.UNDEFINED
            assert clone.get_cell_value(cell_address) is None

    @property
    def _initial_cell_values(self) -> Sequence[Sequence[Optional[int]]]:
        return [
            [4, 1, _, _, _, _, _, _, _],
            [7, _, _, _, _, _, _, _, _],
            [_, _, 4, _, _, _, _, _, _],
            [_, _, _, _, _, _, 3, _, _],
            [_, _, _, _, 9, _, _, _, _],
            [_, _, _, _, _, _, _, _, _],
            [_, 1, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, 8, _, _],
            [_, _, _, _, _, _, _, _, _],
        ]

    @property
    def _modification_list(self) -> Sequence[Tuple[CellAddress, int]]:
        return [
            (get_cell_address(0, 5), 6),
            (get_cell_address(7, 0), 3),
            (get_cell_address(3, 3), 2),
            (get_cell_address(5, 6), 6),
            (get_cell_address(8, 5), 2)
        ]

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
from itertools import product
from typing import List, Tuple


@dataclass(frozen=True)
class CellAddress:
    """
    Immutable structure whose instance represents the coordinates (i.e. row and column) of a single
    cell in a Sudoku grid. The coordinates are zero-based - zero corresponds to the first row or
    column, eight corresponds to the last row or column.
    """
    row: int
    column: int


_all_cell_addresses = tuple([CellAddress(row, column) for row, column in product(range(9), range(9))])


def get_all_cell_addresses() -> Tuple[CellAddress, ...]:
    """
    Returns an immutable collection of CellAddress instances (singletons) corresponding to all 81 cells of
    the Sudoku grid.
    """
    return _all_cell_addresses


def get_cell_address(row: int, column: int) -> CellAddress:
    """
    Returns the cell address singleton for the given cell coordinates.

    Args:
        row (int):       The row coordinate of the cell whose cell address is to be
                         returned. The value zero corresponds to the first row, the
                         value eight corresponds to the last (ninth) row.
        column (int):    The column coordinate of the cell whose cell address is to be
                         returned. The value zero corresponds to the first column, the
                         value eight corresponds to the last (ninth) column.
    
    Returns:
        CellAddress:    The cell address representing the given coordinates.
    """
    return _all_cell_addresses[9 * row + column]


_ImmutablePeerList = Tuple[CellAddress, ...]


def _create_row_peer_addresses_for_single_cell(row: int, column: int) -> List[CellAddress]:
    result = []
    for i in range(0, 9):
        if i != column:
            result.append(get_cell_address(row, i))
    return result


def _create_column_peer_addresses_for_single_cell(row: int, column: int) -> List[CellAddress]:
    result = []
    for i in range(0, 9):
        if i != row:
            result.append(get_cell_address(i, column))
    return result


def _get_upper_left_cell_address_for_region(row: int, column: int) -> CellAddress:
    topmost_row = 3 * (row // 3)
    leftmost_column = 3 * (column // 3)
    return get_cell_address(topmost_row, leftmost_column)


def _create_region_peer_addresses_for_single_cell(row: int, column: int) -> List[CellAddress]:
    upper_left_region_cell = _get_upper_left_cell_address_for_region(row, column)
    result = []
    for r in range(upper_left_region_cell.row, upper_left_region_cell.row + 3):
        for c in range(upper_left_region_cell.column, upper_left_region_cell.column + 3):
            if r != row and c != column:
                result.append(get_cell_address(r, c))
    return result


def _create_peer_addresses_for_single_cell(row: int, column: int) -> _ImmutablePeerList:
    result = _create_row_peer_addresses_for_single_cell(row, column)
    result += _create_column_peer_addresses_for_single_cell(row, column)
    result += _create_region_peer_addresses_for_single_cell(row, column)
    return tuple(set(result))


def _create_peer_addresses_for_single_row(row: int) -> Tuple[_ImmutablePeerList, ...]:
    result = []
    for column in range(0, 9):
        result.append(_create_peer_addresses_for_single_cell(row, column))
    return tuple(result)


def _create_peer_addresses() -> Tuple[Tuple[_ImmutablePeerList, ...], ...]:
    result = []
    for row in range(0, 9):
        result.append(_create_peer_addresses_for_single_row(row))
    return tuple(result)


_peer_addresses = _create_peer_addresses()


def get_peer_addresses(cell_address: CellAddress) -> Tuple[CellAddress, ...]:
    """
    Returns an immutable collection of addresseses of all cells which are peers of the cell with the
    given cell address. Cells residing in the same row, or in the same column, or in the same region as
    the given cell are considered its peers.
    """
    return _peer_addresses[cell_address.row][cell_address.column]

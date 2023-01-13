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
from typing import List, Tuple
from pytest import mark

from sudoku.grid import CellAddress
from sudoku.grid import get_cell_address, get_peer_addresses


@dataclass(frozen=True)
class RegionPeersTestCaseParams:
    cell_address: CellAddress
    expected_peer_coorindates: List[Tuple[int, int]]


class TestCellAddress:
    """
    Test fixture aimed at the class CellAddress and the related global functions.
    """

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_two_cell_addresses_with_the_same_coordinates_are_equal(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates

        assert CellAddress(row, column) == CellAddress(row, column)

    def test_two_cell_addresses_with_the_same_row_but_distinct_columns_are_not_equal(self) -> None:
        assert CellAddress(3, 7) != CellAddress(3, 5)

    def test_two_cell_addresses_with_the_same_column_but_distinct_rows_are_not_equal(self) -> None:
        assert CellAddress(1, 2) != CellAddress(4, 2)

    def test_two_cell_addresses_with_distinct_rows_and_columns_are_not_equal(self) -> None:
        assert CellAddress(5, 4) != CellAddress(3, 8)

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_cell_address_singleton_has_proper_cell_coordinates(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates
        cell_address = get_cell_address(row, column)

        assert cell_address.row == row
        assert cell_address.column == column

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_cell_address_for_any_coordinates_is_singleton(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates
        ref_1 = get_cell_address(row, column)
        ref_2 = get_cell_address(row, column)
        ref_3 = get_cell_address(row, column)

        assert ref_1 is ref_2
        assert ref_1 is ref_3
        assert ref_2 is ref_3

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_any_cell_has_twenty_peers(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates
        peer_addresses = get_peer_addresses(get_cell_address(row, column))

        assert len(peer_addresses) == 20

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_peers_for_any_cell_involve_row_peers(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates
        peer_addresses = get_peer_addresses(get_cell_address(row, column))
        for c in range(0, 9):
            if c != column:
                assert get_cell_address(row, c) in peer_addresses

    @mark.parametrize("cell_coordinates", [(0, 0), (0, 8), (8, 0), (8, 8), (2, 5), (7, 4), (6, 8)])
    def test_peers_for_any_cell_involve_column_peers(self, cell_coordinates: Tuple[int, int]) -> None:
        row, column = cell_coordinates
        peer_addresses = get_peer_addresses(get_cell_address(row, column))
        for r in range(0, 9):
            if r != row:
                assert get_cell_address(r, column) in peer_addresses

    @mark.parametrize("params", [
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(1, 1),
            expected_peer_coorindates=[(0, 0), (0, 2), (2, 0), (2, 2)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(2, 3),
            expected_peer_coorindates=[(0, 4), (0, 5), (1, 4), (1, 5)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(0, 8),
            expected_peer_coorindates=[(1, 6), (1, 7), (2, 6), (2, 7)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(3, 0),
            expected_peer_coorindates=[(4, 1), (4, 2), (5, 1), (5, 2)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(5, 5),
            expected_peer_coorindates=[(3, 3), (3, 4), (4, 3), (4, 4)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(4, 6),
            expected_peer_coorindates=[(3, 7), (5, 8), (3, 7), (5, 8)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(6, 1),
            expected_peer_coorindates=[(7, 0), (8, 2), (7, 0), (8, 2)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(8, 4),
            expected_peer_coorindates=[(6, 3), (7, 5), (6, 3), (7, 5)]
        ),
        RegionPeersTestCaseParams(
            cell_address=get_cell_address(7, 8),
            expected_peer_coorindates=[(6, 6), (8, 7), (6, 6), (8, 7)]
        ),
    ])
    def test_peers_for_any_cell_involve_region_peers(self, params: RegionPeersTestCaseParams) -> None:
        peer_addresses = get_peer_addresses(params.cell_address)
        for row, column in params.expected_peer_coorindates:
            assert get_cell_address(row, column) in peer_addresses

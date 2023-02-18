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
from typing import List, Optional, Sequence, Tuple

from .cell_address import CellAddress
from .cell_address import get_cell_address
from .cell_status import CellStatus


_logger = getLogger(__name__)


class _Cell:

    __slots__ = "_value", "_status"

    """
    Immutable structure whose instance represents a single cell of a Sudoku grid. As this class is
    immutable, single instance of this class can be used by many grids simultaneously, even in
    a multi-threaded environment.
    This class is internal - it is not meant to be used outside of this module.
    """

    def __init__(self, status: CellStatus, value: Optional[int] = None) -> None:
        self._value = value
        self._status = status

    @property
    def value(self) -> int:
        """ The value of the cell represented by this object. """
        assert self._status != CellStatus.UNDEFINED, f"Cell with status {self._status} does not have value."
        return self._value   # type: ignore

    @property
    def status(self) -> CellStatus:
        """ The status of the cell represented by this object. """
        return self._status

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, status={self._status})"


def _create_cells(status: CellStatus) -> Tuple[_Cell, ...]:
    # dummy element at the index 0 eliminates the need to shift the index when
    # accessing the cells by cell value, so this is a minor optimization
    cells = [None] + [_Cell(status, value) for value in range(1, 10)]
    return tuple(cells)  # type: ignore


class _CellSingletons:
    """
    Internal helper class providing access to the instances of the _Cell class.
    """

    _undefined_cell: _Cell = _Cell(CellStatus.UNDEFINED)

    _predefined_cells: Tuple[_Cell, ...] = _create_cells(CellStatus.PREDEFINED)

    _completed_cells: Tuple[_Cell, ...] = _create_cells(CellStatus.COMPLETED)

    @staticmethod
    def get_undefined_cell() -> _Cell:
        """
        Returns the undefined cell singleton.
        """
        return _CellSingletons._undefined_cell

    @staticmethod
    def get_predefined_cell(value: int) -> _Cell:
        """
        Returns the predefined cell singleton with the given cell value.
        """
        return _CellSingletons._predefined_cells[value]

    @staticmethod
    def get_completed_cell(value: int) -> _Cell:
        """
        Returns the completed cell singleton with the given cell value.
        """
        return _CellSingletons._completed_cells[value]


_ValidationBlock = Tuple[CellAddress, ...]


def _create_row_validation_block(row: int) -> _ValidationBlock:
    cell_addresses = [get_cell_address(row, column) for column in range(9)]
    return tuple(cell_addresses)


def _create_column_validation_block(column: int) -> _ValidationBlock:
    cell_addresses = [get_cell_address(row, column) for row in range(9)]
    return tuple(cell_addresses)


def _create_region_validation_block(topmost_row: int, leftmost_column: int) -> _ValidationBlock:
    row_range = range(topmost_row, topmost_row + 3)
    column_range = range(leftmost_column, leftmost_column + 3)
    cell_addresses = [get_cell_address(row, column) for row in row_range for column in column_range]
    return tuple(cell_addresses)


def _create_validation_blocks() -> Tuple[_ValidationBlock, ...]:
    rows = [_create_row_validation_block(row) for row in range(9)]
    columns = [_create_column_validation_block(column) for column in range(9)]
    regions = [
        _create_region_validation_block(top_row, left_column) for top_row in [0, 3, 6] for left_column in [0, 3, 6]
    ]
    return tuple(rows + columns + regions)


CellValues = Sequence[Sequence[Optional[int]]]


class Grid:
    """
    Object-oriented representation of Sudoku grid. Besides the cell values, this grid also keeps
    track of the status of each cell, so it is able to distinguish whether a cell is empty (i.e.
    undefined), if it was predefined (i.e. its value was defined by the original puzzle), or if
    its value has been completed during the search (i.e. it was not predefined, but it is not
    empty anymore). In order to prevent excessive memory consumption and time-consuming cloning
    of grids, an immutable singleton is used to represent each combination of status and value.
    In concrete terms, there are 9 singletons for predefined cells, 9 singletons for completed
    cells, plus one singleton for undefined cell. An unlimited number of grids can safely share
    these singleton objects to represent their cells. Cloning of a grid does not have to clone
    the objects representing the cells, it is enough to clone the collection containing the
    cell objects.
    """

    __slots__ = "_cells", "_undefined_cell_count"

    _validation_blocks = _create_validation_blocks()

    def __init__(self, cell_values: Optional[CellValues] = None, original: Optional[Grid] = None) -> None:
        """
        Constructs a new instance of this class, either using the given initial cell values, or as a copy
        of the given grid.

        Args:
            cell_values (Optional[CellValues]):     The initial cell values. None is to be used if a copy
                                                    of the given grid is to be created.
            original (Grid):                        Original grid whose clone is to be created. None is to
                                                    be used if the created grid is to be initialized from the
                                                    given initial cell values..
        """
        if Grid._is_ordinary_constructor(cell_values, original):
            self._cells, self._undefined_cell_count = Grid._create_cells(cell_values)  # type: ignore
        elif Grid._is_copy_constructor(cell_values, original):
            self._cells = [original._cells[row].copy() for row in range(0, 9)]  # type: ignore
            self._undefined_cell_count = original._undefined_cell_count  # type: ignore
        else:
            message = "Invalid arguments. Exactly one of the two arguments is expected."
            raise ValueError(message)

    @staticmethod
    def _is_ordinary_constructor(cell_values: Optional[CellValues], original: Optional[Grid]) -> bool:
        return original is None and isinstance(cell_values, list)

    @staticmethod
    def _is_copy_constructor(cell_values: Optional[CellValues], original: Optional[Grid]) -> bool:
        return cell_values is None and isinstance(original, Grid)

    @staticmethod
    def _create_cells(cell_values: CellValues) -> Tuple[List[List[_Cell]], int]:
        cells = []
        undefined_cell_count = 0
        for row in range(0, 9):
            row_cells = []
            for column in range(0, 9):
                cell = Grid._convert_to_cell(cell_values[row][column])
                if cell.status == CellStatus.UNDEFINED:
                    undefined_cell_count += 1
                row_cells.append(cell)
            cells.append(row_cells)
        return (cells, undefined_cell_count)

    @staticmethod
    def _convert_to_cell(value: Optional[int]) -> _Cell:
        if value is None:
            return _CellSingletons.get_undefined_cell()
        return _CellSingletons.get_predefined_cell(value)

    @property
    def undefined_cell_count(self) -> int:
        """ The number of undefined cells within this grid. """
        return self._undefined_cell_count

    def get_cell_value(self, cell_address: CellAddress) -> Optional[int]:
        """
        Returns the value of the cell with the given coordinates.

        Args:
            cell_address (CellAddress): The cell address of the cell whose value is to be returned.

        Returns:
            int: The value of the cell with given cell address. None is returned if the cell with
                 the given cell address is undefined.
        """
        if self._cells[cell_address.row][cell_address.column].status == CellStatus.UNDEFINED:
            return None
        return self._cells[cell_address.row][cell_address.column].value

    def get_cell_status(self, cell_address: CellAddress) -> CellStatus:
        """
        Returns the status of the cell with the given coordinates.

        Args:
            cell_address (CellAddress): The cell address of the cell whose status is to be returned.

        Returns:
            CellStatus: The status of the cell with given cell address.
        """
        return self._cells[cell_address.row][cell_address.column].status

    def is_valid(self) -> bool:
        """
        Verifies whether this grid is valid. An incomplete grid (i.e. grid with at least
        one undefined cell) is also valid if it does not violate the Sudoku rules.

        Returns:
            bool: True if and only if none of the rows, none of the columns, and none of the regions
                  of this grid contains a duplicate value; False if this grid contains at least one row,
                  column, or region containing at least one duplicate value.
        """
        for single_validation_block in self._validation_blocks:
            if not self._is_valid(single_validation_block):
                return False
        return True

    def _is_valid(self, validation_block: _ValidationBlock) -> bool:
        used_cell_values = set()
        for cell_address in validation_block:
            cell_status = self.get_cell_status(cell_address)
            if cell_status == CellStatus.UNDEFINED:
                continue
            cell_value = self.get_cell_value(cell_address)
            if cell_value in used_cell_values:
                _logger.error("%d used twice in validation block %s", cell_value, validation_block)
                return False
            used_cell_values.add(cell_value)
        return True

    def is_complete(self) -> bool:
        """
        Verifies whether each and every cell contained in this grid has a value.
        This method does not care about validity. In other words, a grid without
        any empty cell is considered complete even if two cells within a row,
        column or region contain the same value.

        Returns:
            bool: True if and only if none of the cells of this grid is empty; False if
                  this grid contains at least one empty value.
        """
        return self._undefined_cell_count == 0

    def set_cell_value(self, cell_address: CellAddress, value: int) -> None:
        """
        Sets the cell with the given coordinates to the given value, assumed the
        cell with the given coordinates is empty (i.e. its value is undefined).

        Args:
            cell_address (CellAddress): The coordinates of the cell whose value is to be set.
            value (int):                The new value for the given cell.

        Raises:
            ValueError: If the cell with the given coordinates is not empty (i.e. if it already
                        has a value).
        """
        row, column = cell_address.row, cell_address.column
        _logger.debug("Going to set the value of cell [%d, %d] to %d", row, column, value)
        cell = self._cells[row][column]
        if cell.status is not CellStatus.UNDEFINED:
            _logger.error("Cell [%d, %d] not empty (status = %s), going to raise an error", row, column, cell.status)
            message = f"Cannot modify the cell [{row}, {column}] as its state is {cell.status} "
            message += f"(current cell value = {cell.value}, value to be set = {value})."
            raise ValueError(message)
        self._cells[row][column] = _CellSingletons.get_completed_cell(value)
        self._undefined_cell_count -= 1

    def copy(self) -> Grid:
        """
        Creates and returns a copy of this grid which behaves as if it was a deep copy
        of this grid.

        Returns:
            Grid: The created clone of this grid. Be aware of the fact that the returned
                  grid is semantically equivalent to deep copy of this grid. In other words,
                  any modification of the clone will not change the status of this grid and
                  vice versa.
        """
        return Grid(original=self)

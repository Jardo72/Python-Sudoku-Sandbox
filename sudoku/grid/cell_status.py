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

from enum import Enum, unique


@unique
class CellStatus(Enum):
    """
    Defines possible states of a single cell within a Sudoku grid. The meaning of
    particular enum elements is the following:
    * UNDEFINED indicates that a cell has no value (i.e. it was undefined in the original
      puzzle, and it has not been completed yet).
    * PREDEFINED indicates that a call had a value in the original puzzle.
    * COMPLETED indicates that a cell was undefined in the original puzzle, but it has been
      completed in the meantime (i.e. it has already a value).
    """

    UNDEFINED = 1

    PREDEFINED = 2

    COMPLETED = 3

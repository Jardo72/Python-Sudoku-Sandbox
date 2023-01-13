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
class CandidateQueryMode(Enum):
    """
    Defines options how value exclusion logic can provide candidates for an undefined cell.
    The meaning of particular enum elements is the following:
    * FIRST_UNDEFINED_CELL indicates that the candidates for the first undefined cell
      are to be returned, regardless of how many candidates are applicable to the first
      undefined cell.
    * UNDEFINED_CELL_WITH_LEAST_CANDIDATES indicates that the candidates for the
      undefined cell with least applicable candidates are to be returned.
    """

    FIRST_UNDEFINED_CELL = 1

    UNDEFINED_CELL_WITH_LEAST_CANDIDATES = 2

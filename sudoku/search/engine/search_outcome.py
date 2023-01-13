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
class SearchOutcome(Enum):
    """
    Defines possible outcomes of a search. The meaning of particular enum elements is
    the following:
    * SOLUTION_FOUND indicates that the search for a solution has been successful (i.e.
      complete and valid grid derived from the original puzzle has been found).
    * PUZZLE_DEAD_END indicates that the search for solution has failed (i.e. the used
      search algorithm has failed to find complete and valid grid derived from the original
      puzzle), and the failure seems to be caused by the puzzle rather than by the
      limitations of the used search algorithm (i.e. other search algorithm is unlikely to
      find a solution for the puzzle). Assignment dead end means that there is at least one
      undefined cell, but no candidate is applicable to the cell as all values are already
      present in the corresponding row, column, or region (i.e. all 9 values are already
      excluded for the undefined cell).
    * ALGORITHM_DEAD_END indicates that the search for solution has failed (i.e. the
      used search algorithm has failed to find complete and valid grid derived from
      the original puzzle, and the failure might be caused by limitations of the used
      search algorithm (i.e. other search algorithm might be able to find a solution.
      Algorithm dead end means that for each of the undefined cells, there are two
      or more applicable candidate values. In other words, chances are there is a
      solution for the puzzle, but the used search algorithm is unable to cope with
      ambiguity.
    * TIMEOUT indicates that the search for solution has failed due to timeout. In other
      words, the timeout for the search has already expired, and the used search algorithm
      has not found complete and valid grid derived from the original puzzle yet.
    """

    SOLUTION_FOUND = 1

    PUZZLE_DEAD_END = 2

    ALGORITHM_DEAD_END = 3

    TIMEOUT = 4

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

from unittest.mock import Mock, MagicMock, PropertyMock

from sudoku.search.algorithms.dfs import _SearchGraphNode, _SearchGraphNodeStack


def _new_exhausted_mock_node(id: int = None) -> Mock:
    stub = Mock(_SearchGraphNode, name="EX-" + id if id else None)
    stub.already_exhausted.return_value = True
    return stub


def _new_unexhausted_mock_node(id: int = None, remaining_value_count: int = 1) -> MagicMock:
    stub = MagicMock(_SearchGraphNode, name="UNEX-" + id if id else None)
    type(stub).already_exhausted = PropertyMock(side_effect=[False] * remaining_value_count + [True])
    return stub


class TestSearchGraphNodeStack:
    """
    Test fixture aimed at the _SearchGraphNodeStack class.
    """

    def test_backtrack_with_empty_virgin_stack_returns_none(self) -> None:
        stack = _SearchGraphNodeStack()
        assert stack.backtrack_to_first_unexhausted_node() is None

    def test_backtrack_with_stack_containing_only_exhausted_nodes_returns_none(self) -> None:
        stack = _SearchGraphNodeStack()

        stack.push(_new_exhausted_mock_node())
        stack.push(_new_exhausted_mock_node())
        stack.push(_new_exhausted_mock_node())

        assert stack.backtrack_to_first_unexhausted_node() is None

    def test_backtrack_with_stack_containing_two_or_more_unexhausted_nodes_returns_the_topmost_unexhausted_node(self) -> None:
        unexhausted_node_one = _new_unexhausted_mock_node()
        unexhausted_node_two = _new_unexhausted_mock_node()
        stack = _SearchGraphNodeStack()

        stack.push(_new_exhausted_mock_node())
        stack.push(_new_exhausted_mock_node())
        stack.push(unexhausted_node_one)
        stack.push(unexhausted_node_two)

        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_two

    def test_backtracking_preserves_lifo_semantics(self) -> None:
        unexhausted_node_one = _new_unexhausted_mock_node("A")
        unexhausted_node_two = _new_unexhausted_mock_node("B")
        unexhausted_node_three = _new_unexhausted_mock_node("C")
        stack = _SearchGraphNodeStack()

        stack.push(_new_exhausted_mock_node("D"))
        stack.push(_new_exhausted_mock_node("E"))
        stack.push(unexhausted_node_one)
        stack.push(unexhausted_node_two)
        stack.push(_new_exhausted_mock_node("F"))
        stack.push(unexhausted_node_three)

        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_three
        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_two
        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_one
        assert stack.backtrack_to_first_unexhausted_node() is None

    def test_node_with_several_remaining_values_is_returned_repeatedly_until_exhausted(self) -> None:
        unexhausted_node_one = _new_unexhausted_mock_node("A", remaining_value_count=2)
        unexhausted_node_two = _new_unexhausted_mock_node("B", remaining_value_count=3)
        stack = _SearchGraphNodeStack()

        stack.push(unexhausted_node_one)
        stack.push(_new_exhausted_mock_node("C"))
        stack.push(unexhausted_node_two)

        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_two
        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_two
        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_two

        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_one
        assert stack.backtrack_to_first_unexhausted_node() is unexhausted_node_one

        assert stack.backtrack_to_first_unexhausted_node() is None

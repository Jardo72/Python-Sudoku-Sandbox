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

from importlib import import_module
from logging import getLogger
from pkgutil import iter_modules
from typing import Callable, Dict, Tuple, Type

from .abstract_search_algorithm import AbstractSearchAlgorithm
from .no_such_algorithm_error import NoSuchAlgorithmError


_logger = getLogger(__name__)


class SearchAlgorithmRegistry:
    """
    Registry aware of all available search algorithms. This class serves also as a factory
    able to instantiate the search algorithms.
    """

    _entries: Dict[str, Type] = {}

    @staticmethod
    def get_available_algorithms() -> Tuple[str, ...]:
        """
        Creates and returns a tuple containing the names of all search algorithms this
        class is aware of (and thus can instantiate).

        Returns:
            Tuple containing the names of all search algorithms this class is aware of.
            Each of the names contained in the returned tuple can be used as algorithm
            name and passed to the create_algorithm_instance method.
        """
        return tuple(SearchAlgorithmRegistry._entries.keys())

    @staticmethod
    def create_algorithm_instance(algorithm_name: str) -> AbstractSearchAlgorithm:
        """
        Creates and returns a new instance of the search algorithm with the given name.

        Parameters:
            algorithm_name (str):      The name of the search algorithm to be instantiated.

        Returns:
            (AbstractSearchAlgorithm): The created instance of the specified search algorithm.

        Raises:
            NoSuchAlgorithmError:      If there is no search algorithm with the given name.
        """
        if algorithm_name not in SearchAlgorithmRegistry._entries:
            _logger.error("No algorithm with the name %s found", algorithm_name)
            available_algorithms = ", ".join(SearchAlgorithmRegistry._entries.keys())
            message = f"Unknown search algorithm {algorithm_name} has been requested. " \
                f"Available search algorithms: {available_algorithms}."
            raise NoSuchAlgorithmError(message)
        algorithm_class = SearchAlgorithmRegistry._entries[algorithm_name]
        _logger.info("Going to instantiate %s (name = %s)", algorithm_class.__name__, algorithm_name)
        return algorithm_class()


def search_algorithm(name: str) -> Callable:
    """
    Decorator that is to be used to annotate (and automatically register) classes implementing search algorithms.
    """
    def factory(cls: Type) -> Callable:
        _logger.info(f"Going to register algorithm {name} -> {cls.__name__}")
        SearchAlgorithmRegistry._entries[name] = cls

        def decorator() -> Callable:
            return cls
        return decorator
    return factory


def discover_search_algorithms() -> None:
    """
    This function is to be invoked during the initialization of the application. It ensures that
    all search algorithm implementations will be automatically registered in SearchAlgorithmRegistry.
    """
    import sudoku.search.algorithms

    package = sudoku.search.algorithms
    for module_info in iter_modules(package.__path__):
        if module_info.ispkg:
            continue
        module_name = f"{package.__name__}.{module_info.name}"
        import_module(module_name)

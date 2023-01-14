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

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from logging import basicConfig, INFO
from logging.config import fileConfig
from os.path import isfile
from traceback import print_exc

from colorama import init as init_colorama

from sudoku.grid import Grid
from sudoku.io import InvalidInputError
from sudoku.io import read_from_file, render_as_html, render_as_text
from sudoku.search.engine import InvalidPuzzleError, NoSuchAlgorithmError, SearchAlgorithmRegistry, SearchSummary
from sudoku.search.engine import discover_search_algorithms, find_solution


def setup_logging() -> None:
    config_file = "logging-config.ini"
    if isfile(config_file):
        fileConfig(config_file)
        return

    basicConfig(
        level=INFO,
        format="%(asctime)s %(levelname)-8s %(module)-18s line %(lineno)-4d %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
        filename="python-sudoku-sandbox.log",
        filemode="w"
    )


def init() -> None:
    init_colorama()
    setup_logging()
    discover_search_algorithms()


def epilog() -> str:
    return """
The following snippet illustrates the expected format of the input file
containing a puzzle to be solved.
+-------+-------+-------+
| 6     |     4 |   8 5 |
| 9 7   |   6 5 |       |
|   4 8 | 7 3   |       |
+-------+-------+-------+
|   8   | 2 4 7 |       |
|     6 |   8   | 5     |
|       | 1 5 6 |   4   |
+-------+-------+-------+
|       |   1 3 | 2 6   |
|       | 6 9   |   3 4 |
| 2 6   | 4     |     9 |
+-------+-------+-------+
"""


def available_algorithms_as_csv() -> str:
    return ", ".join(SearchAlgorithmRegistry.get_available_algorithms())


def create_command_line_arguments_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Python Sudoku Sandbox", epilog=epilog(), formatter_class=RawTextHelpFormatter)

    # positional mandatory arguments
    parser.add_argument(
        "input_file",
        help="the name of the input file containing the puzzle to be solved"
    )
    parser.add_argument(
        "algorithm",
        help="the name of the search algorithm to be used; available search algorithms are " + available_algorithms_as_csv()
    )

    # optional arguments
    parser.add_argument(
        "-o", "--output-html",
        dest="output_html_file",
        default=None,
        help="the optional name of HTML output file the solution is to be written to"
    )
    parser.add_argument(
        "-t", "--timeout-sec",
        dest="timeout_sec",
        default=60,
        help="the optional timeout in seconds; 60 seconds is used as default if this argument is omitted",
        type=int
    )
    parser.add_argument(
        "-c", "--no-color",
        dest="no_color",
        default=False,
        action="store_true",
        help="if specified, the output will not use any colors"
    )

    return parser


def parse_command_line_arguments() -> Namespace:
    parser = create_command_line_arguments_parser()
    params = parser.parse_args()
    return params


def section_separator() -> str:
    return "=" * 75


def print_search_request(params: Namespace) -> None:
    print()
    print(section_separator())
    print(f"Input file:       {params.input_file}")
    print(f"Output HTML file: {params.output_html_file}")
    print(f"Search algorithm: {params.algorithm}")
    print(f"Timeout:          {params.timeout_sec} sec")
    print()


def print_search_summary(search_summary: SearchSummary, use_color: bool) -> None:
    print()
    print(section_separator())
    print(f"Number of undefined cells in the puzzle: {search_summary.original_undefined_cell_count}")
    print(f"Search algorithm:                        {search_summary.algorithm}")
    print(f"Search outcome:                          {search_summary.outcome}")
    print(f"Search duration:                         {search_summary.duration_millis} ms")
    print(f"Number of tried cell values:             {search_summary.cell_values_tried}")
    print()
    print(render_as_text(search_summary.final_grid, use_color))
    print()
    if not search_summary.final_grid.is_valid():
        print("ERROR!!!")
        print("The final grid is not valid, there is at least one duplicate in a row, in a column, or in a region.")
        print()


def generate_html_file(search_summary: SearchSummary, filename: str) -> None:
    with open(filename, "w") as output_file:
        html_content = render_as_html(search_summary)
        output_file.write(html_content)


def main() -> None:
    try:
        init()
        command_line_arguments = parse_command_line_arguments()
        print_search_request(command_line_arguments)
        puzzle_cell_values = read_from_file(command_line_arguments.input_file)
        search_summary = find_solution(puzzle_cell_values, command_line_arguments.algorithm, command_line_arguments.timeout_sec)
        print_search_summary(search_summary, use_color=not command_line_arguments.no_color)
        if command_line_arguments.output_html_file:
            generate_html_file(search_summary, command_line_arguments.output_html_file)
    except InvalidInputError as e:
        print()
        print(f"Failed to parse the input file {command_line_arguments.input_file}: {str(e)}")
    except (InvalidPuzzleError, NoSuchAlgorithmError) as e:
        print()
        print(f"Puzzle rejected by the search engine: {str(e)}")
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        print()
        print(f"Failed to read puzzle from {command_line_arguments.input_file}")
        print()
        print_exc()
    except (ValueError, RuntimeError, AssertionError, Exception):
        print()
        print_exc()
    finally:
        print()


if __name__ == "__main__":
    main()

"""Handles CLI commands parsing.
"""
from argparse import ArgumentParser, Namespace
from typing import Any


def create_parser() -> ArgumentParser:
    """Returns instance of the `ArgumentParser`

    Returns:
        ArgumentParser: [description]
    """
    return ArgumentParser(description="Elections 2021 API shell handler.")


def create_subparsers(parser: ArgumentParser) -> ArgumentParser:
    """Creates subparsers and return `ArgumentParser` instance.

    Args:
        parser (ArgumentParser): argument parser instance

    Returns:
        ArgumentParser: instance
    """
    subparsers: Any = parser.add_subparsers()

    parser_county: ArgumentParser = subparsers.add_parser(
        "county", help="parser for county/city level data."
    )
    parser_county.add_argument(
        "nuts",
        action="store",
        type=str,
        help="NUTS classifier code value.",
    )
    parser_county.add_argument(
        "--name",
        action="store",
        type=str,
        required=False,
        help="County/City name, if you want to output not whole NUTS, \
        but only concrete city/county.",
    )

    parser_state: ArgumentParser = subparsers.add_parser(
        "state", help="parser for state level data."
    )
    parser_state.add_argument(
        "--district",
        action="store",
        type=int,
        help="If provided, outputs data for given region. Otherwise\
            data for state level are displayed.\n\
            Range is 1 - 14 inclusive.",
    )

    return parser


def parse(parser: ArgumentParser, *args) -> Namespace:
    """Parses CLI args, returns `Namespace` with parsed args.

    Args:
        parser (ArgumentParser): instance

    Returns:
        Namespace: object with parsed args
    """
    return parser.parse_args(*args)

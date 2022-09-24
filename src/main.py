"""Main.
"""
from argparse import Namespace
from time import sleep
from typing import Callable

from src.api import get_county_data, get_state_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.output import clear_screen, enable_coloring, handle_sigint, print_colored_data
from src.parser import parse_county_data, parse_state_data, parse_xml

config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]
resource_state = config["api"]["resources"]["vysledky_stat_kraje"]


def main():
    """Main func."""
    handle_sigint()
    looper(worker)


def looper(worker_: Callable) -> None:
    """Loops the code inside.

    Args:
        worker_ (Callable): worker func.
    """
    index: int = 0
    while True:
        index += 1
        worker_()
        sleep(600)
        clear_screen()
        print(f"Polled for {str(index + 1)} time\n")


def worker():
    """worker func."""

    def wrapper(
        api_func: Callable,
        general_parser: Callable,
        data_specific_parser: Callable,
        printer: Callable,
        **kwargs,
    ) -> None:
        status, raw_data = api_func(**kwargs)

        if status:
            status, parsed_data = general_parser(raw_data)

            if status:
                processed_data = data_specific_parser(parsed_data, **kwargs)
                printer(processed_data)
            else:
                raise RuntimeError(f"{parsed_data}")

        else:
            raise RuntimeError(f"{raw_data}")

    enable_coloring()
    parsed: Namespace = parse(create_subparsers(create_parser()))

    if hasattr(parsed, "nuts"):
        city_name = parsed.name if parsed.name is not None else None
        return wrapper(
            get_county_data,
            parse_xml,
            parse_county_data,
            print_colored_data,
            nuts=parsed.nuts,
            resource=resource_county,
            city=city_name,
        )

    return wrapper(
        get_state_data,
        parse_xml,
        parse_state_data,
        print_colored_data,
        resource=resource_state,
    )

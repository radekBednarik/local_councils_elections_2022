# pylint: disable=expression-not-assigned, redefined-builtin

"""Handles output of data in the console.
"""
from signal import signal, SIGINT
from subprocess import CompletedProcess, run
from sys import platform, exit
from typing import Any, Optional, Union

from colorama import Fore, Style, init

# pylint: disable=unused-argument
def _handler(signum, frame):
    if signum == SIGINT:
        exit()


# pylint: enable=unused-argument


def handle_sigint():
    """Handles SIGINT and cleanly exits without stacktrace."""
    signal(SIGINT, _handler)


def clear_screen() -> Optional[CompletedProcess]:
    """Clears the console."""
    if platform.startswith("linux"):
        return run("clear", shell=True, check=True)

    if platform.startswith("win32"):
        return run("cls", shell=True, check=True)

    return None


def enable_coloring() -> None:
    """Starts the coloring using Colorama.

    Should be called at the beginning of the `main()`.

    See https://github.com/tartley/colorama#initialisation
    """
    init()


def color_green(string: str) -> str:
    """Colors the string GREEN.

    Args:
        string (str): string to be colored green.

    Returns:
        str: colored string
    """
    return f"{Fore.GREEN}{string}{Style.RESET_ALL}"


def color_blue(string: str) -> str:
    """Colors the string BLUE.

    Args:
        string (str): string to be colored

    Returns:
        str: colored string
    """
    return f"{Fore.BLUE}{string}{Style.RESET_ALL}"


def color_cyan(string: str) -> str:
    """Colors the string CYAN.

    Args:
        string (str): string to be colored

    Returns:
        str: colored string
    """
    return f"{Fore.CYAN}{string}{Style.RESET_ALL}"


def print_colored_data(data: Union[dict[str, Any], list[Any]]) -> None:
    """Stdout colored `data` dict.

    Args:
        data (Union[dict[str, Any], list[Any]]): data dict to be recursively
        stdout to console.
    """
    forbidden: list[str] = ["KSTRANA", "VSTRANA", "NAZ_STR"]

    if isinstance(data, list):
        for item in data:
            print_colored_data(item)
            print("-------------")

    if isinstance(data, dict):
        items = list(data.items())

        for key, value in items:
            if not isinstance(value, (dict, list)) and (key not in forbidden):
                print(color_cyan(key), "::", color_green(value))
                continue

            print_colored_data(value)

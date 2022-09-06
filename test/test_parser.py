# pylint: disable=missing-class-docstring, invalid-name, no-self-use, missing-function-docstring
"""Testing parser functions.
"""

from typing import Any

from src.api import get_county_data
from src.io import load_config
from src.parser import parse_xml

config: dict[str, Any] = load_config()
county: str = config["api"]["resources"]["vysledky_okresy_obce"]


class TestParser:
    def test_parser_returns_true(self):
        api_status, raw_data = get_county_data(nuts="CZ0100", resource=county)
        assert api_status is True
        parse_status, _ = parse_xml(raw_data)
        assert parse_status is True

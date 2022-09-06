# pylint: disable=missing-class-docstring, invalid-name, no-self-use, missing-function-docstring
"""Handles tests of API functions.
"""

from typing import Any

from hamcrest import is_, assert_that, contains_string, instance_of
from requests import Response
from src.api import call, get_county_data, get_state_data
from src.io import load_config

config: dict[str, Any] = load_config()
root: str = config["api"]["root"]
county: str = config["api"]["resources"]["vysledky_okresy_obce"]
state: str = config["api"]["resources"]["vysledky_stat_kraje"]


class TestApi:
    def test_call(self):
        full_resource = county.replace(r"{{nuts}}", "CZ0100")
        response = call(full_resource, root)
        assert_that(response, instance_of(Response))

    def test_get_county_data(self):
        status, raw_data = get_county_data(nuts="CZ0100", resource=county)
        assert_that(status, is_(True))
        assert_that(raw_data, instance_of(str))

    def test_validate(self):
        status, raw_data = get_county_data(nuts="CZ01", resource=county)
        assert_that(status, is_(False))
        assert_that(raw_data, contains_string("<CHYBA>"))

    def test_get_state_data(self):
        status, raw_data = get_state_data(state)
        assert_that(status, is_(True))
        assert_that(raw_data, instance_of(str))

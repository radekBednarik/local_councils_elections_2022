# pylint: disable=missing-class-docstring, invalid-name, no-self-use, missing-function-docstring, redefined-outer-name

"""E2E tests.
"""

from hamcrest import assert_that, instance_of, is_, not_
from pytest import fixture
from src.api import get_county_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.parser import parse_county_data, parse_xml

config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]


@fixture(params=[["county", "CZ0100"]])
def parsed_input(request):
    return parse(create_subparsers(create_parser()), request.param)


class TestE2E:
    def test_e2e(self, parsed_input):
        # get data from api call
        pass

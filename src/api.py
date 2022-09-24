"""Handles API calls to opend data XML data source.
"""

import sys
from time import sleep

from requests import Response, get

from src.decorators import cache
from src.utils import replace_substring, retrieve_error_message


def call(
    resource: str, root_: str = "https://www.volby.cz", counter: int = 0
) -> Response:
    """Calls the web resource and returns response.

    Response is `requests.Response` object

    Args:
        resource (str): resource part of API URL
        root (str, optional): root part of the API URL. Defaults to `https://www.volby.cz`.
        counter (int, optional): used for recursive call in case of request failure

    Returns:
        Response: requests object representing response
    """
    limit: int = 10
    try:
        response: Response = get(f"{root_}{resource}")
        response.raise_for_status()
        return response
    except Exception as exc:
        if counter < limit:
            counter += 1
            print(
                f"Error when trying to call the endpoint. Waiting for {counter} seconds.... Try {counter} out of {limit}"
            )
            sleep(counter)
            call(resource, counter=counter)
        else:
            print(f"[!] ERROR when calling {resource}: {exc}")
            sys.exit(1)


def validate(response_text: str, start_tag: str = "<CHYBA>") -> tuple[bool, str]:
    """Checks, whether there is error message in retrieved XML data.

    Args:
        response_text (str): data from the response body as str
        start_tag (str, optional): tag marking the beginning of the XML error message.
        Defaults to "<CHYBA>".

    Returns:
        tuple[bool, str]: status of the validation, and either error message, or the data
    """
    if start_tag in response_text:
        return (False, retrieve_error_message(response_text))
    return (True, response_text)


# pylint: disable=unused-argument


@cache(time_delta=60, location="cache.tmp", resource_template=r"{{nuts}}")
def get_county_data(
    nuts: str = None, resource: str = None, **kwargs
) -> tuple[bool, str]:
    """Returns data of given `nuts` county as `str`. This needs to be
    further parsed by XML parser.

    Args:
        nuts (Optional[str]): NUTS code of given county/city.
        resource (Optional[str]): resource template url.

    Returns:
        tuple[bool, str]: if data does not contain error message, return `(True, data)`.
        Else return `(False, error message)`.
    """
    if nuts is not None and resource is not None:
        full_resource: str = replace_substring(resource, nuts, r"{{nuts}}")
        response: Response = call(full_resource)
        status, text = validate(response.text)
        return (status, text)
    raise TypeError("Arguments can be only of type {str}!")


@cache(time_delta=60, location="cache.tmp", resource_template=None)
def get_state_data(resource: str = None, **kwargs) -> tuple[bool, str]:
    """Returns data from the state level as `str`. This needs to be
    further parsed by XML parser.

    Args:
        resource (str, optional): resource URL. Defaults to None.

    Raises:
        TypeError: if resource is None

    Returns:
        tuple[bool, str]: if data does not contain error message, return `(True, data)`.
        Else return `(False, error_message)`
    """
    if resource is not None:
        response: Response = call(resource)
        status, text = validate(response.text)
        return (status, text)
    raise TypeError("Argument can be only of type {str}!")


# pylint: enable=unused-argument

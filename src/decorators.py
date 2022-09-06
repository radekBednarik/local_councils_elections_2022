"""Decorator funcs are here.
"""

from typing import Any, Callable, Optional, Union

from src.io import process_cache, read_psrkl


def cache(**kwargs):
    """Caches the api call.

    Args:
        time_delta: (int, Optional) how long to cache and thus return cached data. Defaults to `60`.
        location: (str, Optional) location of the cache file. Defaults to `cache.tmp`
        resource_template: (str, Optional) string template to be replaced from the resource URL
        by the actual value. Defaults to `{{nuts}}`
    """

    def inner(
        func,
        time_delta: int = kwargs["time_delta"],
        location: str = kwargs["location"],
        resource_template: Optional[str] = kwargs["resource_template"],
    ):
        def wrapper(*args, **kwargs):
            return process_cache(
                time_delta, location, func, resource_template, *args, **kwargs
            )

        return wrapper

    return inner


def add_party_name(func) -> Union[Callable, dict[str, Any]]:
    """Adds party name to parsed data from xml, using `pskrl.csv` classifier content.

    It is not universal function and expect exact data structure, namely:

    ```
    parsed_data_to_be_modified = {"main_key": {"classifiers":{...}, "data":[{}, {}, ...]}}
    ```

    where `dict` in data `list` contains key `KSTRANA`.

    Args:
        func (Callable): XML data parser/convertor to `dict` data type

    Raises:
        RuntimeError: in case parsed data are returned with `Falsy` value

    Returns:
        dict[str, Any]: original parsed XML data as dict with added `STRANA` key and value pair.
    """
    psrkl: dict[str, dict[str, str]] = read_psrkl()

    def wrapper(*args, **kwargs) -> dict[str, Any]:
        parsed_data: dict[str, Any] = func(*args, **kwargs)
        if parsed_data:
            master_key: str = list(list(parsed_data.keys()))[0]
            data: list[dict[str, str]] = parsed_data[master_key]["data"]

            for index, item in enumerate(data):
                for key, value in list(item.items()):
                    if key == "KSTRANA":
                        parsed_data[master_key]["data"][index]["STRANA"] = psrkl[value][
                            "ZKRATKAK8"
                        ]

            return parsed_data
        raise RuntimeError("Parsed data are empty!")

    return wrapper

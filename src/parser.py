# pylint: disable= c-extension-no-member, broad-except

"""Handles the parsing of the XML data.
"""

from typing import Any, Optional

from lxml import etree


def parse_xml(
    xml_string_data: str, encoding: str = "utf-8"
) -> tuple[bool, Optional[Any]]:
    """Parses the XML formatted raw string data and returns representation
    as `root` node.

    Parser is `lxml`.

    String is encoded before parsing to `utf-8`, since XML has this encoding
    declaration, and `lxml` would throw otherwise. Encoding can be changed.

    Args:
        xml_string_data (str): XML data to be parsed.
        encoding (str, optional): Into which encoding the raw data string should be encoded into.
        Defaults to "utf-8".

    Returns:
        tuple[bool, Optional[Any]]: Parsed data.
    """
    try:
        parsed = etree.fromstring(xml_string_data.encode(encoding))
        return (True, parsed)
    except Exception as exc:
        print(str(exc))
        return (False, None)


def nested_loops(
    level_1: Any, output: dict[str, Any], master_key: str
) -> dict[str, Any]:
    """Runs thru all nested lists of parsed xml data, appends
    them to the `output` dict and returns the dict.

    Args:
        level_1 (Any): lxml Element object representing the first level of the data
        output (dict[str, Any]): final data output as `dict`
        master_key (str): first key of the output `dict`

    Returns:
        dict[str, Any]: parsed nested xml data, flattened inside `list` of
        the output `dict`
    """
    for level_x in list(level_1):
        output[master_key]["data"].append(dict(level_x.attrib))
        nested_loops(level_x, output, master_key)

    return output


# pylint: disable=unused-argument


def parse_county_data(
    parsed_data: Any, city: Optional[str] = None, **kwargs
) -> dict[str, Any]:
    """Parses XML object to retrieve data as `dict`.

    In case the `city` name from given NUTS county is not provided,
    then data for NUTS county level are returned.

    In case the `city` name is provided, data for given city are returned.

    Args:
        parsed_data (Any): lxml Element object representing XML data
        city (Optional[str], optional): Name of the city from the county
        E.g. "Praha 1". Defaults to None.

    Returns:
        dict[str, Any]: parsed data from lxml Element object as `dict`.
    """
    output: dict[str, Any] = {}
    authorities_data_level: list[Any] = list(parsed_data)
    master_key: str = ""

    for level_1 in authorities_data_level:
        if city is None and "OBEC" in level_1.tag:
            master_key = level_1.attrib["KODZASTUP"]
            output[master_key] = {"descriptors": dict(level_1.attrib), "data": []}

            return nested_loops(level_1, output, master_key)

        if (
            city is not None
            and "OBEC" in level_1.tag
            and city.strip() == level_1.attrib["NAZEVZAST"]
        ):
            master_key = level_1.attrib["KODZASTUP"]
            output[master_key] = {"descriptors": dict(level_1.attrib), "data": []}

            return nested_loops(level_1, output, master_key)

    return output


def parse_state_data(parsed_data: Any, **kwargs) -> dict[str, Any]:
    """Parses XML object to retrieve data as `dict`.

    Args:
        parsed_data (Any): lxml Element object representing XML data

    Returns:
        dict[str, Any]: parsed data as `dict`.
    """
    output: dict[str, Any] = {}
    top_level_data: list[Any] = list(parsed_data)
    master_key: str = ""

    try:
        for level_1 in top_level_data:
            master_key = level_1.attrib["OZNAC_TYPU"]
            output[master_key] = {"data": []}
            nested_loops(level_1, output, master_key)
        return output
    except RuntimeError as exc:
        raise RuntimeError(f"State level XML data were not parsed!: {exc}") from exc


# pylint: enable=unused-argument

"""Utilities.
"""


def retrieve_error_message(data: str, start_tag: str = "<CHYBA>") -> str:
    """Retrieves error message from the data str body.

    Args:
        data (str): data body
        start_tag (str, optional): XML tag marking the beginning of the error message.
        Defaults to "<CHYBA>".

    Raises:
        IndexError: if Error message is corrupted, e.g not properly encoded via expected
        tags, function will throw an IndexError.

    Returns:
        str: error message
    """
    end_tag: str = "".join([start_tag[0], "/", start_tag[1:]])

    start_index: int = data.find(start_tag)
    end_index: int = data.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise IndexError("Error message from data could not be retrieved.")

    return data[start_index : end_index + len(end_tag)]


def replace_substring(string: str, substring: str, template: str) -> str:
    """Replaces template substring for substring in the string.

    Returns the string.

    Args:
        string (str): string with templated, which should be replaced
        by substring
        substring (str): substring to replace the template
        template (str): template to be replaced by substring

    Returns:
        str: string with substring instead of the template
    """
    return string.replace(template, substring)

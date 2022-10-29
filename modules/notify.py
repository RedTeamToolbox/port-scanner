# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import modules.constants as PSconstants


def success(message: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_
    """

    print(f"{PSconstants.SUCCESS}{message}{PSconstants.RESET}")


def success_msg(message: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """

    return f"{PSconstants.SUCCESS}{message}{PSconstants.RESET}"


def warn(message: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_
    """

    print(f"{PSconstants.WARN}{message}{PSconstants.RESET}")


def warn_msg(message: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """

    return f"{PSconstants.WARN}{message}{PSconstants.RESET}"


def error(message: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_
    """
    print(f"{PSconstants.ERROR}{message}{PSconstants.RESET}")


def error_msg(message: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{PSconstants.ERROR}{message}{PSconstants.RESET}"


def info(message: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_
    """
    print(f"{PSconstants.INFO}{message}{PSconstants.RESET}")


def info_msg(message: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{PSconstants.INFO}{message}{PSconstants.RESET}"

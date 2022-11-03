# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from .constants import ERROR, INFO, RESET, SUCCESS, WARN


def success(message: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_
    """
    print(f"{SUCCESS}{message}{RESET}")


def success_msg(message: str) -> str:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{SUCCESS}{message}{RESET}"


def warn(message: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_
    """
    print(f"{WARN}{message}{RESET}")


def warn_msg(message: str) -> str:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{WARN}{message}{RESET}"


def error(message: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_
    """
    print(f"{ERROR}{message}{RESET}")


def error_msg(message: str) -> str:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{ERROR}{message}{RESET}"


def info(message: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_
    """
    print(f"{INFO}{message}{RESET}")


def info_msg(message: str) -> str:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        message (str) -- _description_

    Returns:
        str -- _description_
    """
    return f"{INFO}{message}{RESET}"

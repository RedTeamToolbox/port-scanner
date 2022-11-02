# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from argparse import _ArgumentGroup, SUPPRESS
from typing import Any, ContextManager

from alive_progress import alive_bar

from .constants import CLI_HELP


def get_help_text(command_name: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        command_name (str) -- _description_

    Returns:
        str -- _description_
    """
    if command_name in CLI_HELP:
        return CLI_HELP[command_name]
    return "There is no help available"


def add_help_flag(group: _ArgumentGroup) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        group (_ArgumentGroup) -- _description_
    """
    group.add_argument("-h", "--help", action="help", default=SUPPRESS, help=get_help_text("help"))


def add_cli_flag(group: _ArgumentGroup, short_name: str, long_name: str, default_value: bool = False) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        group (_ArgumentGroup) -- _description_
        short_name (str) -- _description_
        long_name (str) -- _description_

    Keyword Arguments:
        default_value (bool) -- _description_ (default: False)
    """
    group.add_argument(short_name, long_name, action="store_true", default=default_value, help=get_help_text(long_name.replace('-', '')))


def add_cli_argument(group: _ArgumentGroup, short_name: str, long_name: str, type_name: Any, default_value: Any = None) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        group (_ArgumentGroup) -- _description_
        short_name (str) -- _description_
        long_name (str) -- _description_
        type_name (Any) -- _description_

    Keyword Arguments:
        default_value (Any) -- _description_ (default: None)
    """
    group.add_argument(short_name, long_name, type=type_name, default=default_value, help=get_help_text(long_name.replace('-', '')))


def create_spinner(title: str) -> ContextManager:
    """_summary_

    _extended_summary_

    Keyword Arguments:
        title (str) -- _description_ (default: None)

    Returns:
        ContextManager -- _description_
    """
    return alive_bar(title = title, stats = False, monitor = False, stats_end = False, receipt = True, bar = None)


def create_alive_bar(size: int, title: str, length: int = 80) -> ContextManager:
    """_summary_

    _extended_summary_

    Arguments:
        size (int) -- _description_
        title (str) -- _description_

    Keyword Arguments:
        length (int) -- _description_ (default: 80)

    Returns:
        ContextManager -- _description_
    """

    return alive_bar(size, title = title, length = length)

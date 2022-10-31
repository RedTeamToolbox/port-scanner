# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from typing import ContextManager

from alive_progress import alive_bar


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

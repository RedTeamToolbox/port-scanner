# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from .globals import secrets_generator


def secure_random(min_number: int, max_number: int) -> int:
    """_summary_.

    _extended_summary_

    Arguments:
        min_number (int) -- _description_
        max_number (int) -- _description_

    Returns:
        _type_ -- _description_
    """
    return secrets_generator.randint(min_number, max_number)

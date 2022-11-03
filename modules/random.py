# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from .globals import secrets_generator


def secure_random(min_number: int, max_number: int) -> int:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        min_number (int) -- _description_
        max_number (int) -- _description_

    Returns:
        int -- _description_
    """
    return secrets_generator.randint(min_number, max_number)

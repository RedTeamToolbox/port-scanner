# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import modules.globals as PSglobals


def secure_random(min_number: int, max_number: int) -> int:
    """_summary_

    _extended_summary_

    Arguments:
        min_number (int) -- _description_
        max_number (int) -- _description_

    Returns:
        _type_ -- _description_
    """
    return PSglobals.secretsGenerator.randint(min_number, max_number)

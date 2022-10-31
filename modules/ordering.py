# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from functools import cmp_to_key
from operator import itemgetter
from typing import Any

import modules.globals as PSglobals


def cmp(x, y) -> Any:
    """_summary_

    _extended_summary_

    Arguments:
        x (_type_) -- _description_
        y (_type_) -- _description_

    Returns:
        Any -- _description_
    """
    return (x > y) - (x < y)


def multikeysort(items: list[dict], columns: list[str]) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        items (list[dict]) -- _description_
        columns (list[str]) -- _description_

    Returns:
        list[dict] -- _description_
    """
    comparers = [
        ((itemgetter(col[1:].strip()), -1) if col.startswith("-") else (itemgetter(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right) -> int:
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def shuffled(things: list[Any], depth: int = 1) -> list[Any]:
    """_summary_

    _extended_summary_

    Arguments:
        things (list[Any]) -- _description_

    Keyword Arguments:
        depth (int) -- _description_ (default: 1)

    Returns:
        list[Any] -- _description_
    """
    results = []

    if depth == 0:
        return things

    for sublist in things:
        if isinstance(sublist, list):
            results.append(shuffled(sublist, depth - 1))
        else:
            results.append(sublist)
    results = PSglobals.secretsGenerator.sample(results, len(results))
    return results

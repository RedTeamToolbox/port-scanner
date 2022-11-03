# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from functools import cmp_to_key
from operator import itemgetter
from typing import Any, Generator

from .globals import secrets_generator


def cmp(left, right) -> Any:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        left (_type_) -- _description_
        right (_type_) -- _description_

    Returns:
        Any -- _description_
    """
    return (left > right) - (left < right)


def multikeysort(items: list[dict], columns: list[str]) -> list[dict]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        items (list[dict]) -- _description_
        columns (list[str]) -- _description_

    Returns:
        list[dict] -- _description_
    """
    comparers: list = [
        ((itemgetter(col[1:].strip()), -1) if col.startswith("-") else (itemgetter(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right) -> int:
        comparer_iter: Generator = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def shuffled(things: list[Any], depth: int = 1) -> list[Any]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        things (list[Any]) -- _description_

    Keyword Arguments:
        depth (int) -- _description_ (default: 1)

    Returns:
        list[Any] -- _description_
    """
    results: list = []

    if depth == 0:
        return things

    for sublist in things:
        if isinstance(sublist, list):
            results.append(shuffled(sublist, depth - 1))
        else:
            results.append(sublist)
    results = secrets_generator.sample(results, len(results))
    return results

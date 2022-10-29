# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import secrets
import sys

from functools import cmp_to_key
from operator import itemgetter
from typing import Any

from tqdm import tqdm


secretsGenerator = secrets.SystemRandom()


def secure_random(min_number: int, max_number: int):
    """_summary_

    _extended_summary_

    Arguments:
        min_number (int) -- _description_
        max_number (int) -- _description_

    Returns:
        _type_ -- _description_
    """
    return secretsGenerator.randint(min_number, max_number)


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
    results = secretsGenerator.sample(results, len(results))
    return results


def create_bar(prefix: str, size: int, color: str = "cyan", leave: bool = True):
    """_summary_

    _extended_summary_

    Arguments:
        prefix (str) -- _description_
        size (int) -- _description_

    Keyword Arguments:
        color (str) -- _description_ (default: "cyan")
        leave (bool) -- _description_ (default: True)

    Returns:
        _type_ -- _description_
    """
    bar_format = f"{prefix} |{{bar:80}}| {{percentage:3.2f}}% [{{n_fmt}} of {{total}}] [Run: {{elapsed}} ETA: {{remaining}}]"

    return tqdm(total=size, bar_format=bar_format, colour=color, leave=leave)

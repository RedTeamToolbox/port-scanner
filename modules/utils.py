"""
A set of utility functions
"""

import secrets

from functools import cmp_to_key
from operator import itemgetter
from typing import Any

secretsGenerator = secrets.SystemRandom()


def secure_random(min, max):
    """
    docs
    """
    return secretsGenerator.randint(min, max)


def cmp(x, y) -> Any:
    """
    Docs
    """
    return (x > y) - (x < y)


def multikeysort(items: list[dict], columns: list[str]) -> list[dict]:
    """
    Docs
    """
    comparers = [
        ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right) -> int:
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def shuffled(things, depth = 1):
    """
    Simple function to shuffle the order of a list
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

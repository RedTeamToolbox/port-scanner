# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from tqdm import tqdm


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

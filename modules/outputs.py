# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import csv
import json

from types import SimpleNamespace
from typing import Any
from prettytable import PrettyTable

from .ordering import multikeysort


def save_results_as_csv(results: list[dict], fname: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        results (list[dict]) -- _description_
        fname (str) -- _description_
    """
    if len(results) == 0:
        return

    with open(f"{fname}.csv", "w", encoding="utf-8") as outfile:
        csv_writer: Any = csv.writer(outfile)
        columns: list[str] = ['target', 'ip', 'port', 'service', 'status_string', 'banner', 'error']
        csv_writer.writerow(columns)
        for row in results:
            csv_writer.writerow([None if column not in row else row[column] for column in columns])


def save_results_as_json(results: list[dict], fname: str) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        results (list[dict]) -- _description_
        fname (str) -- _description_
    """
    if len(results) == 0:
        return

    with open(f"{fname}.json", "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4, default=str)


def print_table_of_results(results: list[dict]) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        results (list[dict]) -- _description_
    """
    table: PrettyTable = PrettyTable()

    table.field_names = ["Target", "IP", "Port", "Service", "Open?", "Banner", "Errors"]

    for parts in results:
        table.add_row([
            parts['target'],
            parts['ip'],
            parts['port'],
            parts['service'],
            parts['status'],
            parts['banner'],
            parts['error']
        ])
    print(table)


def process_results(results: list[dict], all_results: bool = True) -> list[dict]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        results (list[dict]) -- _description_

    Keyword Arguments:
        all_results (bool) -- _description_ (default: True)

    Returns:
        list[dict] -- _description_
    """
    processed_results: list[dict] = results
    if all_results is False:
        processed_results = [i for i in results if i['status'] is True]
    return multikeysort(processed_results, ['target', 'ipnum', 'port'])


def display_results(results: list[dict], config: SimpleNamespace) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        results (list[dict]) -- _description_
        args (_type_) -- _description_
    """
    processed_results: list[dict] = process_results(results, config.all_results)

    # TODO Save the results in cache files?
    if config.quiet is False:
        print_table_of_results(processed_results)

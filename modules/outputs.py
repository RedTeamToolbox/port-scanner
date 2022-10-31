# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import csv
import json

from prettytable import PrettyTable

import modules.config as PSconfig
import modules.ordering as PSOrdering


def save_results_as_csv(results: list[dict], fname: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        results (list[dict]) -- _description_
        fname (str) -- _description_
    """
    if len(results) == 0:
        return

    with open(f"{fname}.csv", "w", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        columns = ['target', 'ip', 'port', 'service', 'status_string', 'banner', 'error']
        writer.writerow(columns)
        for row in results:
            writer.writerow([None if column not in row else row[column] for column in columns])


def save_results_as_json(results: list[dict], fname: str) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        results (list[dict]) -- _description_
        fname (str) -- _description_
    """
    if len(results) == 0:
        return

    with open(f"{fname}.json", "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4, default=str)


def print_table_of_results(results: list[dict]) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        results (list[dict]) -- _description_
    """
    table = PrettyTable()

    table.field_names = ["Target", "IP", "Port", "Service", "Open?", "Banner", "Errors"]

    for parts in results:
        table.add_row([parts['target'], parts['ip'], parts['port'], parts['service'], parts['status'], parts['banner'], parts['error']])
    print(table)


def process_results(results: list[dict], all_results = True) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        results (list[dict]) -- _description_

    Keyword Arguments:
        all_results (bool) -- _description_ (default: True)

    Returns:
        list[dict] -- _description_
    """
    if all_results is False:
        results = [i for i in results if i['status'] is True]
    return PSOrdering.multikeysort(results, ['target', 'ipnum', 'port'])


def display_results(results: list[dict], config: PSconfig.Configuration) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        results (list[dict]) -- _description_
        config (PSconfig.Configuration) -- _description_
    """
    results = process_results(results, config.all_results)

    # TODO Save the results in cache files?
    if config.quiet is False:
        print_table_of_results(results)

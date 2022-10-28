"""
Code for handling results processing
"""

import csv
import json

from prettytable import PrettyTable

import modules.config as PSconfig
import modules.utils as PSutils


def save_results_as_csv(results: list[dict], fname: str) -> None:
    """
    Docs
    """
    if len(results) == 0:
        return

    with open(f"{fname}.csv", "w", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        columns = list({column for row in results for column in row.keys()})
        writer.writerow(columns)
        for row in results:
            writer.writerow([None if column not in row else row[column] for column in columns])


def save_results_as_json(results: list[dict], fname: str) -> None:
    """
    Docs
    """
    if len(results) == 0:
        return

    with open(f"{fname}.json", "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4, default=str)


def print_table_of_results(results: list[dict]) -> None:
    """
    Docs
    """
    table = PrettyTable()

    table.field_names = ["Target", "IP", "Port", "Service", "Open?", "Banner", "Errors"]

    for parts in results:
        table.add_row([parts['target'], parts['ip'], parts['port'], parts['service'], parts['status'], parts['banner'], parts['error']])
    print(table)


def process_results(results: list[dict], all_results = True) -> list[dict]:
    """
    docs
    """
    if all_results is False:
        results = [i for i in results if i['status'] is True]
    return PSutils.multikeysort(results, ['target', 'ipnum', 'port'])


def display_results(results: list[dict], config: PSconfig.Configuration) -> None:
    """
    Docs
    """
    results = process_results(results, config.all_results)

    if config.csv is True:
        save_results_as_csv(results, config.filename)
    if config.json is True:
        save_results_as_json(results, config.filename)
    if config.quiet is False:
        print_table_of_results(results)

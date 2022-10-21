#!/usr/bin/env python

"""
stuff
"""

import argparse
import csv
import json
import ipaddress
import itertools
import re
import secrets
import socket
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import cmp_to_key
from operator import itemgetter
from time import sleep
from typing import Any

import colored
import dns.resolver

from colored import stylize
from prettytable import PrettyTable
from yaspin import yaspin

secretsGenerator = secrets.SystemRandom()
host_ip_mapping = {}
service_name_mapping = {}


def save_results_as_csv(args: argparse.Namespace, results: list[dict]) -> None:
    """
    Docs
    """
    with open(f'{args.filename}.csv', 'w', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        columns = list({column for row in results for column in row.keys()})
        writer.writerow(columns)
        for row in results:
            writer.writerow([None if column not in row else row[column] for column in columns])


def save_results_as_json(args: argparse.Namespace, results: list[dict]) -> None:
    """
    Docs
    """
    with open(f'{args.filename}.json', "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4, default=str)


def print_table_of_results(results: list[dict]) -> None:
    """
    Docs
    """
    table = PrettyTable()

    table.field_names = ['Target', 'IP', 'Port', 'Service', 'Open?']

    for parts in results:
        table.add_row([parts['target'], parts['ip'], parts['port'], parts['service'], parts['status']])
    print(table)


def display_results(results: list[dict], args) -> None:
    """
    Docs
    """
    if args.csv is True:
        save_results_as_csv(args, results)
    if args.json is True:
        save_results_as_json(args, results)
    if args.quiet is False:
        print_table_of_results(results)


def scan_target_port(target, port, spinner, args: argparse.Namespace) -> dict[str, Any]:
    """
    docs
    """
    status = False

    if args.delay is True:
        sleep_time = secretsGenerator.randint(1, args.delay_time)
        if args.verbose is True:
            spinner.write(stylize(f"Host: sleeping for {sleep_time} seconds", colored.fg("cyan")))
        sleep(sleep_time)

    if args.verbose is True:
        spinner.write(stylize(f"Host: {target} Testing Port: {port}", colored.fg("cyan")))

    ip = ipaddress.ip_address(target)
    if isinstance(ip, ipaddress.IPv6Address) is True:
        af_type = socket.AF_INET6
    else:
        af_type = socket.AF_INET

    with socket.socket(af_type, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((target, port))
            status = True
        except socket.error:
            status = False

    if args.verbose is True:
        spinner.write(stylize(f"Host: {target}, Port: {port}, Open?: {status}", colored.fg("cyan")))

    return {'target': host_ip_mapping[target], 'ip': ip, 'port': port, 'status': status, 'service': service_name_mapping[port]}


def is_ip_address(target: str) -> Any:
    """
    docs
    """
    try:
        ip = ipaddress.ip_address(target)
        status = bool(isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)))
    except ValueError:
        status = False

    return status


def get_records(host, record_type):
    """
    docs
    """
    try:
        resolver_results = dns.resolver.resolve(host, record_type)
        results = [val.to_text() for val in resolver_results]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        results = []

    return results


def get_ips(target):
    """
    docs
    """
    if is_ip_address(target) is False:
        results = sorted(get_records(target, 'A')) + sorted(get_records(target, 'AAAA'))
    else:
        results = [target]
    return results


def validate_targets(targets):
    """
    docs
    """
    global host_ip_mapping  # pylint: disable=global-variable-not-assigned
    valid_targets = []

    for target in targets:
        try:
            for ip in get_ips(target):
                host_ip_mapping[ip] = target
                valid_targets.append(ip)
        except socket.gaierror:
            print(stylize(f"{target} is not valid - Skipping)", colored.fg("yellow")))

    return valid_targets


def get_all_host_port_combinations(targets, ports):
    """
    docs
    """
    return list(itertools.product(targets, ports))


def scan_target(targets: list[tuple], threads: int, args: argparse.Namespace) -> list:
    """
    Docs
    """
    results = []

    if threads > len(targets):
        how_many = len(targets)
    else:
        how_many = threads

    with yaspin(text=stylize(f"Processing host port ({how_many} threads)", colored.fg("green")), timer=True) as spinner:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            futures = [executor.submit(scan_target_port, target[0], target[1], spinner, args) for target in targets]

            for future in as_completed(futures):
                thread_results = future.result()
                if thread_results:
                    results.append(thread_results)

    spinner.ok("✅")

    return results


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


def process_results(results: list[dict], all_results = True):
    """
    docs
    """
    if all_results is False:
        results = [i for i in results if i['status'] is True]

    return multikeysort(results, ['target', 'ip', 'port'])


def get_port_list(args: argparse.Namespace) -> list[int]:
    """
    Docs
    """
    global service_name_mapping  # pylint: disable=global-variable-not-assigned
    ports = []

    for port in args.ports.split(','):
        # Format A-B
        result = re.search(r"(\d+)-(\d+)", port)
        if result is not None:
            ports += (list(range(int(result.group(1)), int(result.group(2)))))
            continue

        # Format A:B
        result = re.search(r"(\d+):(\d+)", port)
        if result is not None:
            ports += (list(range(int(result.group(1)), int(result.group(2)))))
            continue

        # Just a normal number
        if port.isnumeric():
            ports.append(int(port))
            continue

        # Left with a string like sshd
        try:
            ports.append(socket.getservbyname(port))
        except OSError:
            print(stylize(f"{port} is not a valid service name - Skipping!", colored.fg("yellow")))
            continue

    # Now we need to remove any duplicates and sort
    ports = sorted(list(set(ports)))

    # Build the mappings so we dont have to lookup in each return thread - 1 host = no saving 2 or more is N-1 times faster
    for port in ports:
        try:
            service = socket.getservbyport(port, 'tcp')
        except OSError:
            service = 'Unknown'
        service_name_mapping[port] = service

    return ports


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


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """
    Docs
    """
    pass


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Setup the arguments parser to handle the user input from the command line.
    """

    epilog = "Port options: port range e.g. 1-1024 or 1:1024, port number e.g. 22, service name e.g. ssh"

    parser = argparse.ArgumentParser(prog='portscan', description='Check for open ports on target host', add_help=False, epilog=epilog, formatter_class=CustomFormatter)
    flags = parser.add_argument_group('flags')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    flags.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    flags.add_argument('-q', '--quiet', action="store_true", help="Don't show the results on the screen", default=False)
    flags.add_argument('-v', '--verbose', action="store_true", help="Verbose output", default=False)

    required.add_argument('-D', '--delay-time', type=int, help='Random delay to use if --delay is given', default=3)
    required.add_argument('-p', '--ports', type=str, help='The search regex', default="1-1024")
    required.add_argument('-t', '--targets', type=str, help='A comma separated list of targets to scan', required=True)
    required.add_argument('-T', '--threads', type=int, help='The number of threads to use', default=1024)

    optional.add_argument('-a', '--all-results', action="store_true", help="Show all results (default is to list open ports only)", default=False)
    optional.add_argument('-c', '--csv', action="store_true", help="Save the results as a csv formatted file", default=False)
    optional.add_argument('-d', '--delay', action="store_true", help="Add a random delay to each thread", default=False)
    optional.add_argument('-f', '--filename', type=str, help='The filename to save the results to', default='portscan-results')
    optional.add_argument('-j', '--json', action="store_true", help="Save the results as a json formatted file", default=False)
    optional.add_argument('-r', '--random', action="store_true", help="Randomise the scanning order", default=False)

    return parser


def process_arguments() -> argparse.Namespace:
    """
    Main wrapper for handling the arguments, setup, read and validate all before returning to main().
    """

    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.quiet is True and args.json is False and args.csv is False:
        print(stylize("Fatal: You cannot use --quiet unless you supply --csv or --json", colored.fg("red")))
        sys.exit(0)

    with yaspin(text=stylize("Processing arguments", colored.fg("green")), timer=True) as spinner:
        args.ports = get_port_list(args)
        args.targets = args.targets.split(',')
        args.targets = validate_targets(args.targets)
    spinner.ok("✅")

    if not args.targets:
        print(stylize("Fatal: No valid targets were found - Aborting!", colored.fg("red")))
        sys.exit(0)

    return args


def main() -> None:
    """
    The main function.
    """
    args = process_arguments()

    # Take all the ips and ports and get ALL combinations

    with yaspin(text=stylize("Generating host:port combinations", colored.fg("green")), timer=True) as spinner:
        target_list = get_all_host_port_combinations(args.targets, args.ports)
        if args.random is True:
            target_list = shuffled(target_list)
    spinner.ok("✅")

    results = scan_target(target_list, args.threads, args)
    results = process_results(results, args.all_results)
    display_results(results, args)


if __name__ == "__main__":
    main()

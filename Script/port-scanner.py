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
ip_ipnum_mapping = {}
service_name_mapping = {}

port_rules = [
    # mssql server, mssql browser, ingres, mysql, postgresql
    {'rule': 'databases', 'ports': [1433, 1434, 1524, 3306, 5432]},
    # smtp, pop3, imap, submission
    {'rule': 'email', 'ports': [25, 110, 143, 587, 2525]},
    # ftp-data, ftp, tftp
    {'rule': 'file-transfer', 'ports': [20, 21, 69]},
    # name service, datagram service,  session service
    {'rule': 'netbios', 'ports': [137, 138, 139]},
    # ssh, telnet, remote desktop, VNC
    {'rule': 'remote-access', 'ports': [22, 23, 3389, 5900]},
    # samba
    {'rule': 'samba', 'ports': [445]},
    # http, https, http-alt, pcsync-https, pcsync-http
    {'rule': 'web-servers', 'ports': [80, 443, 8080, 8443, 8444]},
]


def save_results_as_csv(args: argparse.Namespace, results: list[dict]) -> None:
    """
    Docs
    """
    if len(results) == 0:
        return

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
    if len(results) == 0:
        return

    with open(f'{args.filename}.json', "w", encoding="utf-8") as outfile:
        json.dump(results, outfile, indent=4, default=str)


def print_table_of_results(results: list[dict]) -> None:
    """
    Docs
    """
    table = PrettyTable()

    table.field_names = ['Target', 'IP', 'Port', 'Service', 'Open?', 'Banner', 'Errors']

    for parts in results:
        table.add_row([parts['target'], parts['ip'], parts['port'], parts['service'], parts['status'], parts['banner'], parts['error']])
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
    global service_name_mapping  # pylint: disable=global-variable-not-assigned
    status = False
    error_msg = None
    banner = None

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
        sock.settimeout(1)
        try:
            sock.connect((target, port))
            status = True
            try:
                banner = sock.recv(2048).decode('utf-8').strip()
            except socket.error as err:
                banner = 'Unavailable'
                error_msg = err
            sock.shutdown(0)
            sock.close()
        except socket.timeout:
            error_msg = "Connection timed out"
            status = False
        except socket.error as err:
            error_msg = str(err)
            result = re.search(r"(\[Errno \d+\] )?(.*)", error_msg)
            if result is not None:
                error_msg = result.group(2)
            status = False

    if args.verbose is True:
        spinner.write(stylize(f"Host: {target}, Port: {port}, Open?: {status}", colored.fg("cyan")))

    # Cache the service name in case we are hitting multiple IPs
    if port not in service_name_mapping:
        try:
            service = socket.getservbyport(port, 'tcp')
        except OSError:
            service = 'Unknown'
        service_name_mapping[port] = service

    return {
            'target': host_ip_mapping[target],
            'ip': ip,
            'ipnum': ip_ipnum_mapping[target],
            'port': port,
            'status': status,
            'service': service_name_mapping[port],
            'banner': banner,
            'error': error_msg
           }


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


def get_ips(target, ipv4_only, ipv6_only):
    """
    docs
    """

    if is_ip_address(target) is False:
        if ipv4_only is True:
            results = sorted(get_records(target, 'A'))
        elif ipv6_only is True:
            results = sorted(get_records(target, 'AAAA'))
        else:
            results = sorted(get_records(target, 'A')) + sorted(get_records(target, 'AAAA'))
    else:
        results = [target]
    return results


def validate_targets(targets, ipv4_only, ipv6_only):
    """
    docs
    """
    global host_ip_mapping  # pylint: disable=global-variable-not-assigned
    global ip_ipnum_mapping  # pylint: disable=global-variable-not-assigned

    valid_targets = []

    for target in targets:
        try:
            for ip in get_ips(target, ipv4_only, ipv6_only):
                if (ip in host_ip_mapping and is_ip_address(target) is False) or ip not in host_ip_mapping:
                    host_ip_mapping[ip] = target
                ip_ipnum_mapping[ip] = int(ipaddress.ip_address(ip))
                valid_targets.append(ip)

        except socket.gaierror:
            print(stylize(f"{target} is not valid - Skipping)", colored.fg("yellow")))

    # Now we need to remove any duplicates and sort
    valid_targets = sorted(list(set(valid_targets)))
    return valid_targets


def get_all_host_port_combinations(targets, ports):
    """
    docs
    """
    return list(itertools.product(targets, ports))


def scan_targets(targets: list[tuple], threads: int, args: argparse.Namespace) -> list:
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
    return multikeysort(results, ['target', 'ipnum', 'port'])


def list_all_port_rules():
    """
    Docs
    """

    print(stylize("Available rule sets:", colored.fg("cyan")))
    count = 0
    for rule in port_rules:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


def get_ports_from_rule(rule_name):
    """
    Docs
    """

    for rule in port_rules:
        if rule['rule'] == rule_name:
            return rule['ports']
    return None


def get_ports_from_rule_sets(rule_sets):
    """
    Docs
    """
    ports = []

    for rule in rule_sets.split(','):
        rule_ports = get_ports_from_rule(rule)
        if rule_ports is not None:
            ports += rule_ports
        else:
            print(stylize(f"{rule} is not a valid ruleset - Skipping!", colored.fg("yellow")))
    return ports


def get_port_list(args: argparse.Namespace) -> list[int]:
    """
    Docs
    """
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

        match_results = re.search(r"ruleset:(.*)", port, re.IGNORECASE)
        if match_results is not None:
            ports += get_ports_from_rule_sets(match_results.group(1))
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

    epilog = "Port options: port range e.g. 1-1024 or 1:1024, port number e.g. 22, rule set e.g. ruleset=web-servers, service name e.g. ssh"

    parser = argparse.ArgumentParser(prog='port-scan', description='Check for open ports on target host', add_help=False, epilog=epilog, formatter_class=CustomFormatter)
    flags = parser.add_argument_group('flags')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    flags.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='show this help message and exit')
    flags.add_argument('-q', '--quiet', action="store_true", help="Do not show the results on the screen", default=False)
    flags.add_argument('-v', '--verbose', action="store_true", help="Verbose output", default=False)
    flags.add_argument('-4', '--ipv4-only', action="store_true", help="Scan IPv4 addresses only", default=False)
    flags.add_argument('-6', '--ipv6-only', action="store_true", help="Scan IPv4 addresses only", default=False)
    flags.add_argument('-A', '--all-results', action="store_true", help="Show or save all results (default is to list open ports only)", default=False)
    flags.add_argument('-c', '--csv', action="store_true", help="Save the results as a csv formatted file", default=False)
    flags.add_argument('-d', '--delay', action="store_true", help="Add a random delay to each thread", default=False)
    flags.add_argument('-j', '--json', action="store_true", help="Save the results as a json formatted file", default=False)
    flags.add_argument('-s', '--shuffle', action="store_true", help="Randomise the scanning order", default=False)
    flags.add_argument('-r', '--list-rules', action="store_true", help="List the available rules", default=False)

    required.add_argument('-t', '--targets', type=str, help='A comma separated list of targets to scan')

    optional.add_argument('-D', '--delay-time', type=int, help='Random delay to use if --delay is given', default=3)
    optional.add_argument('-p', '--ports', type=str, help='The ports you want to scan', default="1-1024")
    optional.add_argument('-e', '--exclude-ports', type=str, help='The ports you want to exclude from a scan')
    optional.add_argument('-T', '--threads', type=int, help='The number of threads to use', default=1024)
    optional.add_argument('-f', '--filename', type=str, help='The filename to save the results to', default='portscan-results')

    return parser


def process_arguments() -> argparse.Namespace:
    """
    Main wrapper for handling the arguments, setup, read and validate all before returning to main().
    """

    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.list_rules is True:
        list_all_port_rules()
        sys.exit(0)

    if args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        print(stylize("Fatal: You cannot use --quiet unless you supply --csv or --json", colored.fg("red")))
        sys.exit(0)

    if args.quiet is True and args.ipv4_only is False and args.ipv6_only is False:
        print(stylize("Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!", colored.fg("red")))
        sys.exit(0)

    with yaspin(text=stylize("Generating Port list", colored.fg("green")), timer=True) as spinner:
        args.ports = get_port_list(args)
    spinner.ok("✅")
    if len(args.ports) == 0:
        print(stylize("Fatal: No valid ports were found - Aborting!", colored.fg("red")))
        sys.exit(0)

    # Change this to be single host!
    with yaspin(text=stylize("Generating IP target list", colored.fg("green")), timer=True) as spinner:
        args.targets = args.targets.split(',')
        args.targets = validate_targets(args.targets, args.ipv4_only, args.ipv6_only)
    spinner.ok("✅")

    if not args.targets:
        print(stylize("Fatal: No valid targets were found - Aborting!", colored.fg("red")))
        sys.exit(0)

    return args


def main() -> None:
    """
    The main function.
    """

    # Increase the resource limit ??

    args = process_arguments()

    # Take all the ips and ports and get ALL combinations
    with yaspin(text=stylize("Generating host:port combinations", colored.fg("green")), timer=True) as spinner:
        target_list = get_all_host_port_combinations(args.targets, args.ports)
        if args.shuffle is True:
            target_list = shuffled(target_list)
    spinner.ok("✅")

    results = scan_targets(target_list, args.threads, args)
    results = process_results(results, args.all_results)
    display_results(results, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Exiting Program]")
        sys.exit(0)
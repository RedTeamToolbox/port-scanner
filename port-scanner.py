#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the summary line

Usage:
    ./port-scan.py [-h] [-q] [-v] [-4] [-6] [-A] [-c] [-j] [-s] [-r] [-t TARGETS] [-b BATCH_SIZE] [-B BATCH_DELAY] [-d DELAY_TIME] [-p INCLUDE_PORTS] [-e EXCLUDE_PORTS] [-T THREADS] [-f FILENAME]
"""

import sys

from argparse import _ArgumentGroup, ArgumentParser, Namespace, SUPPRESS

from modules.constants import EPILOG, PORT_RULES
from modules.core import run_scanner
from modules.globals import default_threads
from modules.notify import error, info


def __list_all_port_rules() -> None:
    """_summary_

    _extended_summary_
    """
    info("Available rule sets:")
    count: int = 0
    for rule in PORT_RULES:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


def __setup_arg_parser() -> ArgumentParser:
    """_summary_

    _extended_summary_

    Returns:
        argparse.ArgumentParser -- _description_
    """

    # TODO: this is the list of jobs to do
    # TODO: add a way to define targets as ranges (like with ports) or using CIDR notation
    # TODO: add a way to load ips from file (same as with ports)
    # TODO: add an option to exclude targets incase you are using a range or CIDR
    # TODO: add an option to append to results files ?
    # TODO: store the results as a cache per IP (like the batching system I wrote)
    # TODO: define a cache timeout (default 1 week)
    parser: ArgumentParser = ArgumentParser(prog="port-scan", description="Check for open port(s) on target host(s)", add_help=False, epilog=EPILOG)

    system_flags: _ArgumentGroup = parser.add_argument_group("system flags")
    application_flags: _ArgumentGroup = parser.add_argument_group("application flags")
    required: _ArgumentGroup = parser.add_argument_group("required arguments")
    optional: _ArgumentGroup = parser.add_argument_group("optional arguments")

    system_flags.add_argument("-h", "--help", action="help", default=SUPPRESS, help="show this help message and exit")
    system_flags.add_argument("-q", "--quiet", action="store_true", help="Do not show the results on the screen", default=False)
    system_flags.add_argument("-v", "--verbose", action="store_true", help="Verbose output - show scan results as they come in", default=False)

    application_flags.add_argument("-4", "--ipv4-only", action="store_true", help="Scan IPv4 addresses only", default=False)
    application_flags.add_argument("-6", "--ipv6-only", action="store_true", help="Scan IPv6 addresses only", default=False)
    application_flags.add_argument("-A", "--all-results", action="store_true", help="Show or save all results (default is to list open ports only)", default=False)

    application_flags.add_argument("-s", "--shuffle", action="store_true", help="Randomise the scanning order", default=False)
    application_flags.add_argument("-r", "--list-rules", action="store_true", help="List the available rules", default=False)

    required.add_argument("-t", "--targets", type=str, help="A comma separated list of targets to scan")

    optional.add_argument("-b", "--batch-size", type=int, help="The size of the batch to use when splitting larger scan sets (0 = no batching)", default=0)
    optional.add_argument("-B", "--batch-delay", type=int, help="The amount of time to wait between batches", default=60)
    optional.add_argument("-d", "--delay-time", type=int, help="Random delay to use if --delay is given", default=3)
    optional.add_argument("-p", "--include-ports", type=str, help="The ports you want to scan", default="1-1024")
    optional.add_argument("-e", "--exclude-ports", type=str, help="The ports you want to exclude from a scan")
    optional.add_argument("-T", "--threads", type=int, help="The number of threads to use", default=default_threads)
    optional.add_argument("-f", "--filename", type=str, help="The filename to save the results to", default="portscan-results")

    return parser


def process_command_line_arguments() -> Namespace:
    """_summary_

    _extended_summary_

    Returns:
        argparse.Namespace -- _description_
    """

    parser: ArgumentParser = __setup_arg_parser()
    args: Namespace = parser.parse_args()

    if args.list_rules is True:
        __list_all_port_rules()
        sys.exit(0)

    if args.include_ports is None:
        parser.print_help()
        sys.exit(0)

    if args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        error("Fatal: You cannot use --quiet unless you supply --csv or --json")
        sys.exit(0)

    if args.quiet is True and args.ipv4_only is False and args.ipv6_only is False:
        error("Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!")
        sys.exit(0)

    return args


def main() -> None:
    """The main function.

    This is the main function for the port scanner. It has been kept intentionally as small as possible and just
    defines the flow of the program.

    1. Get the arguments from the user.
    2. Create the configuration needed.
    3. Work out what ports needs to be scanned.
    4. Work out what target ips need to be scanned.
    5. Scan the targets / ports.
    6. Process the results.
    7. Exit.
    """

    args: Namespace = process_command_line_arguments()
    run_scanner(args)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        info("\n[*] Exiting Program\n")

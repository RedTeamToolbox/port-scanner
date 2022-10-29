# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import argparse
import multiprocessing
import sys

import modules.constants as PSconstants
import modules.notify as PSnotify
import modules.ports as PSports


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """_summary_

    _extended_summary_

    Arguments:
        argparse (_type_) -- _description_
        argparse (_type_) -- _description_
    """
    pass


def setup_arg_parser() -> argparse.ArgumentParser:
    """_summary_

    _extended_summary_

    Returns:
        argparse.ArgumentParser -- _description_

    TODO:
        add a way to define targets as ranges (like with ports) or using CIDR notation
        add a way to load ips from file (same as with ports)
        add an option to exclude targets incase you are using a range or CIDR
        add an option to append to results files ?
        store the results as a cache per IP (like the batching system I wrote)
        define a cache timeout (default 1 week)
    """
    default_threads = multiprocessing.cpu_count() * 5

    parser = argparse.ArgumentParser(prog="port-scan", description="Check for open port(s) on target host(s)", add_help=False, epilog=PSconstants.EPILOG, formatter_class=CustomFormatter)
    system_flags = parser.add_argument_group("system flags")
    application_flags = parser.add_argument_group("application flags")
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    system_flags.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="show this help message and exit")
    system_flags.add_argument("-q", "--quiet", action="store_true", help="Do not show the results on the screen", default=False)
    system_flags.add_argument("-v", "--verbose", action="store_true", help="Verbose output - show scan results as they come in", default=False)

    application_flags.add_argument("-4", "--ipv4-only", action="store_true", help="Scan IPv4 addresses only", default=False)
    application_flags.add_argument("-6", "--ipv6-only", action="store_true", help="Scan IPv6 addresses only", default=False)
    application_flags.add_argument("-A", "--all-results", action="store_true", help="Show or save all results (default is to list open ports only)", default=False)

    application_flags.add_argument("-c", "--csv", action="store_true", help="Save the results as a csv formatted file", default=False)
    application_flags.add_argument("-j", "--json", action="store_true", help="Save the results as a json formatted file", default=False)
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


def process_arguments() -> argparse.Namespace:
    """_summary_

    _extended_summary_

    Returns:
        argparse.Namespace -- _description_
    """

    parser = setup_arg_parser()
    args = parser.parse_args()

    if args.list_rules is True:
        PSports.list_all_port_rules()
        sys.exit(0)

    if args.include_ports is None:
        parser.print_help()
        sys.exit(0)

    if args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        PSnotify.error("Fatal: You cannot use --quiet unless you supply --csv or --json")
        sys.exit(0)

    if args.quiet is True and args.ipv4_only is False and args.ipv6_only is False:
        PSnotify.error("Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!")
        sys.exit(0)

    return args

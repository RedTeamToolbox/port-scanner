"""
Cli stuff
"""

import argparse
import multiprocessing
import sys

import modules.constants as PSconstants
import modules.notify as PSnotify
import modules.ports as PSports


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """
    Docs
    """
    pass


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Setup the arguments parser to handle the user input from the command line.
    """
    default_threads = multiprocessing.cpu_count() * 5

    parser = argparse.ArgumentParser(prog="port-scan", description="Check for open port(s) on target host(s)", add_help=False, epilog=PSconstants.EPILOG, formatter_class=CustomFormatter)
    flags = parser.add_argument_group("flags")
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")

    flags.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="show this help message and exit")
    flags.add_argument("-q", "--quiet", action="store_true", help="Do not show the results on the screen", default=False)
    flags.add_argument("-v", "--verbose", action="store_true", help="Verbose output - show scan results as they come in", default=False)
    flags.add_argument("-4", "--ipv4-only", action="store_true", help="Scan IPv4 addresses only", default=False)
    flags.add_argument("-6", "--ipv6-only", action="store_true", help="Scan IPv6 addresses only", default=False)
    flags.add_argument("-A", "--all-results", action="store_true", help="Show or save all results (default is to list open ports only)", default=False)
    flags.add_argument("-c", "--csv", action="store_true", help="Save the results as a csv formatted file", default=False)
    flags.add_argument("-d", "--delay", action="store_true", help="Add a random delay to each thread", default=False)
    flags.add_argument("-j", "--json", action="store_true", help="Save the results as a json formatted file", default=False)
    flags.add_argument("-s", "--shuffle", action="store_true", help="Randomise the scanning order", default=False)
    flags.add_argument("-r", "--list-rules", action="store_true", help="List the available rules", default=False)

    required.add_argument("-t", "--targets", type=str, help="A comma separated list of targets to scan")

    optional.add_argument("-b", "--batch-size", type=int, help="The size of the batch to use when splitting larger scan sets (0 = no batching)", default=0)
    optional.add_argument("-B", "--batch-delay", type=int, help="The amount of time to wait between batches in seconds", default=60)
    optional.add_argument("-D", "--delay-time", type=int, help="Random delay to use if --delay is given", default=3)
    optional.add_argument("-p", "--include-ports", type=str, help="The ports you want to scan", default="1-1024")
    optional.add_argument("-e", "--exclude-ports", type=str, help="The ports you want to exclude from a scan")
    optional.add_argument("-T", "--threads", type=int, help="The number of threads to use", default=default_threads)
    optional.add_argument("-f", "--filename", type=str, help="The filename to save the results to", default="portscan-results")

    return parser


def process_arguments() -> argparse.Namespace:
    """
    Main wrapper for handling the arguments, setup, read and validate all before returning to main().
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

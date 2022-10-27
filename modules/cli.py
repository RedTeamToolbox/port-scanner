"""
Cli stuff
"""

import argparse
import sys

import colored
from colored import stylize
from yaspin import yaspin

import modules.constants as PSconstants
import modules.notify as PSnotify
import modules.ports as PSports
import modules.targets as PStargets


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    """
    Docs
    """
    pass


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Setup the arguments parser to handle the user input from the command line.
    """

    parser = argparse.ArgumentParser(prog='port-scan', description='Check for open port(s) on target host(s)', add_help=False, epilog=PSconstants.EPILOG, formatter_class=CustomFormatter)
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
    optional.add_argument('-p', '--include-ports', type=str, help='The ports you want to scan', default="1-1024")
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
        PSports.list_all_port_rules()
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

    with yaspin(text=stylize("Generating target port list", colored.fg("green")), timer=True) as spinner:
        args.include_ports = PSports.get_port_list(args.include_ports)
        if args.exclude_ports is not None:
            args.exclude_ports = PSports.get_port_list(args.exclude_ports)
            if len(args.exclude_ports) > 0:
                args.include_ports = [x for x in args.include_ports if x not in args.exclude_ports]
    spinner.ok("✅")
    if len(args.include_ports) == 0:
        PSnotify.error("Fatal: No valid ports were found - Aborting!")
        sys.exit(0)

    # Change this to be single host!
    with yaspin(text=stylize("Generating IP target list", colored.fg("green")), timer=True) as spinner:
        args.targets = args.targets.split(',')
        args.targets = PStargets.validate_targets(args.targets, args.ipv4_only, args.ipv6_only)
    spinner.ok("✅")

    if not args.targets:
        PSnotify.error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)

    return args

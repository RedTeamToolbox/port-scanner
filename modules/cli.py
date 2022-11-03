# -*- coding: utf-8 -*-
"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import argparse
import multiprocessing
import sys

from .exceptions import InvalidParameters
from .ports import list_all_port_rules


def _add_flags_to_parser(parser: argparse.ArgumentParser) -> None:
    """_summary_.

    _extended_summary_

    Arguments:
        parser (argparse.ArgumentParser) -- _description_
    """
    flags: argparse._ArgumentGroup = parser.add_argument_group(
        title="optional flags",
        description="Description"
    )

    flags.add_argument("-h", "--help",
                       action="help",
                       help="show this help message and exit")
    flags.add_argument("-q", "--quiet",
                       action="store_true", default=False,
                       help="Do not show the results on the screen")
    flags.add_argument("-v", "--verbose",
                       action="store_true", default=False,
                       help="Verbose output - show scan results as they come in")
    flags.add_argument("-V", "--very-verbose",
                       action="store_true", default=False,
                       help="Very noisy and details all connections etc")
    flags.add_argument("-4", "--ipv4-only",
                       action="store_true", default=False,
                       help="Scan IPv4 addresses only")
    flags.add_argument("-6", "--ipv6-only",
                       action="store_true", default=False,
                       help="Scan IPv6 addresses only")
    flags.add_argument("-A", "--all-results",
                       action="store_true", default=False,
                       help="Show or save all results (default is to list open ports only)")
    flags.add_argument("-s", "--shuffle",
                       action="store_true", default=False,
                       help="Randomise the scanning order")
    flags.add_argument("-r", "--list-rules",
                       action="store_true", default=False,
                       help="List the available rules")


def _add_required_parameters(parser: argparse.ArgumentParser) -> None:
    """_summary_.

    _extended_summary_

    Arguments:
        parser (argparse.ArgumentParser) -- _description_
    """
    required: argparse._ArgumentGroup = parser.add_argument_group(
        title="required arguments",
        description="stuff"
    )
    required.add_argument("-t", "--targets",
                          type=str, default=None,
                          help="A comma separated list of targets to scan")
    required.add_argument("-p", "--ports",
                          type=str, default=None,
                          help="The ports you want to scan")


def _add_optional_parameters(parser: argparse.ArgumentParser) -> None:
    """_summary_.

    _extended_summary_

    Arguments:
        parser (argparse.ArgumentParser) -- _description_
    """
    default_threads: int = multiprocessing.cpu_count() * 5

    optional: argparse._ArgumentGroup = parser.add_argument_group(
        title="optional arguments",
        description=""
    )
    optional.add_argument("-b", "--batch-size",
                          type=int, default=0,
                          help="The size of the batch to use when splitting larger scan sets")
    optional.add_argument("-B", "--batch-delay",
                          type=int, default=0,
                          help="The amount of time to wait between batches")
    optional.add_argument("-d", "--delay-time",
                          type=int, default=3,
                          help="Random delay to use if --delay is given")
    optional.add_argument("-e", "--exclude-ports",
                          type=int,
                          help="The ports you want to exclude from a scan")
    optional.add_argument("-T", "--threads",
                          type=int, default=default_threads,
                          help="The number of threads to use")
    optional.add_argument("-c", "--cache-directory",
                          type=str, default="~/.portscan-cache",
                          help="Not Yet Implemented")
    optional.add_argument("-f", "--filename",
                          type=str, default="results",
                          help="Not Yet Implemented")


# TODO: this is the list of jobs to do
# TODO: add a way to define targets as ranges (like with ports) or using CIDR notation
# TODO: add a way to load ips from file (same as with ports)
# TODO: add an option to exclude targets incase you are using a range or CIDR
# TODO: add an option to append to results files ?
# TODO: store the results as a cache per IP (like the batching system I wrote)
# TODO: define a cache timeout (default 1 week)
def _setup_arg_parser() -> argparse.ArgumentParser:
    """_summary_.

    _extended_summary_

    Returns:
        argparse.ArgumentParser -- _description_
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Check for open port(s) on target host(s)",
        epilog="""For detailed documentation please refer to:
                  https://github.com/OffSecToolbox/port-scanner""",
    )
    _add_flags_to_parser(parser)
    _add_required_parameters(parser)
    _add_optional_parameters(parser)

    return parser


def process_command_line_arguments() -> argparse.Namespace:
    """_summary_.

    _extended_summary_

    Raises:
        InvalidParameters: _description_
        InvalidParameters: _description_

    Returns:
        argparse.Namespace -- _description_
    """
    parser: argparse.ArgumentParser = _setup_arg_parser()
    args: argparse.Namespace = parser.parse_args()

    if args.list_rules is True:
        list_all_port_rules()
        sys.exit(0)

    if args.ports is None or args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        raise InvalidParameters("[X] Fatal: You cannot use --quiet without --csv or --json")

    if args.ipv4_only is True and args.ipv6_only is True:
        raise InvalidParameters("[X] Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!")

    return args

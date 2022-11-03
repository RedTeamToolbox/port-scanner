# -*- coding: utf-8 -*-
"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import sys

from argparse import _ArgumentGroup, ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

from .exceptions import InvalidParameters
from .constants import CLI_HELP
from .globals import default_threads
from .ports import list_all_port_rules


def _get_help_text(command_name: str) -> str:
    """_summary_

    _extended_summary_

    Arguments:
        command_name (str) -- _description_

    Returns:
        str -- _description_
    """
    if command_name in CLI_HELP:
        return CLI_HELP[command_name]
    return "There is no help available"


def _add_flags_to_parser(parser: ArgumentParser) -> None:
    flags: _ArgumentGroup = parser.add_argument_group(
        title="optional flags",
        description="Description"
    )

    flags.add_argument("-h", "--help", action="help", help=_get_help_text("help"))
    flags.add_argument("-q", "--quiet", action="store_true", default=False, help=_get_help_text("quiet"))
    flags.add_argument("-v", "--verbose", action="store_true", default=False, help=_get_help_text("verbose"))
    flags.add_argument("-4", "--ipv4-only", action="store_true", default=False, help=_get_help_text("ipv4-only"))
    flags.add_argument("-6", "--ipv6-only", action="store_true", default=False, help=_get_help_text("ipv6-only"))
    flags.add_argument("-A", "--all-results", action="store_true", default=False, help=_get_help_text("all-results"))
    flags.add_argument("-s", "--shuffle", action="store_true", default=False, help=_get_help_text("shuffle"))
    flags.add_argument("-r", "--list-rules", action="store_true", default=False, help=_get_help_text("list-rules"))


def _add_required_parameters(parser: ArgumentParser) -> None:
    required: _ArgumentGroup = parser.add_argument_group(
        title="required arguments",
        description="stuff"
    )
    required.add_argument("-t", "--targets", type=str, help=_get_help_text("targets"))
    required.add_argument("-p", "--include-ports", type=str, help=_get_help_text("include-ports"))


def _add_optional_parameters(parser: ArgumentParser) -> None:
    optional: _ArgumentGroup = parser.add_argument_group("optional arguments")
    optional.add_argument("-b", "--batch-size", type=int, default=0, help=_get_help_text("batch-size"))
    optional.add_argument("-B", "--batch-delay", type=int, default=60, help=_get_help_text("batch-delay"))
    optional.add_argument("-d", "--delay-time", type=int, default=3, help=_get_help_text("delay-time"))
    optional.add_argument("-e", "--exclude-ports", type=int, help=_get_help_text("exclude-ports"))
    optional.add_argument("-T", "--threads", type=int, default=default_threads, help=_get_help_text("threads"))
    optional.add_argument("-f", "--filename", type=str, default="results", help=_get_help_text("filename"))


# TODO: this is the list of jobs to do
# TODO: add a way to define targets as ranges (like with ports) or using CIDR notation
# TODO: add a way to load ips from file (same as with ports)
# TODO: add an option to exclude targets incase you are using a range or CIDR
# TODO: add an option to append to results files ?
# TODO: store the results as a cache per IP (like the batching system I wrote)
# TODO: define a cache timeout (default 1 week)
def _setup_arg_parser() -> ArgumentParser:
    """_summary_

    _extended_summary_

    Returns:
        ArgumentParser -- _description_
    """
    parser: ArgumentParser = ArgumentParser(
        add_help=False,
        formatter_class=ArgumentDefaultsHelpFormatter,
        description="Check for open port(s) on target host(s)",
        epilog="For more detailed documentation please refer to: https://github.com/SecOpsToolbox/port-scanner",
    )
    _add_flags_to_parser(parser)
    _add_required_parameters(parser)
    _add_optional_parameters(parser)

    return parser


def process_command_line_arguments() -> Namespace:
    """_summary_

    _extended_summary_

    Raises:
        InvalidParameters: _description_
        InvalidParameters: _description_

    Returns:
        Namespace -- _description_
    """

    parser: ArgumentParser = _setup_arg_parser()
    args: Namespace = parser.parse_args()

    if args.list_rules is True:
        list_all_port_rules()
        sys.exit(0)

    if args.include_ports is None or args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        raise InvalidParameters("[X] Fatal: You cannot use --quiet unless you supply --csv or --json")

    if args.ipv4_only is True and args.ipv6_only is True:
        raise InvalidParameters("[X] Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!")

    return args

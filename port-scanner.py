#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the summary line

more to follow
"""

import os
import sys

from argparse import _ArgumentGroup, ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace

from modules.constants import CLI_DESC, CLI_EPILOG, PORT_RULES
from modules.core import run_scanner
from modules.exceptions import InvalidParameters
from modules.globals import default_threads
from modules.notify import error, info
from modules.utils import add_cli_argument, add_cli_flag, add_help_flag


def __list_all_port_rules() -> None:
    """_summary_

    _extended_summary_
    """
    info("Available rule sets:")
    count: int = 0
    for rule in PORT_RULES:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


# TODO: this is the list of jobs to do
# TODO: add a way to define targets as ranges (like with ports) or using CIDR notation
# TODO: add a way to load ips from file (same as with ports)
# TODO: add an option to exclude targets incase you are using a range or CIDR
# TODO: add an option to append to results files ?
# TODO: store the results as a cache per IP (like the batching system I wrote)
# TODO: define a cache timeout (default 1 week)
def __setup_arg_parser() -> ArgumentParser:
    """_summary_

    _extended_summary_

    Returns:
        argparse.ArgumentParser -- _description_
    """
    system_flag_list: dict = {
            '-q': '--quiet',
            '-v': '--verbose'
    }
    application_flag_list: dict = {
            '-4': '--ipv4-only',
            '-6': '--ipv6-only',
            '-A': '--all-results',
            '-s': '--shuffle',
            '-r': '--list-rules',
    }

    parser: ArgumentParser = ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                            description=CLI_DESC,
                                            epilog=CLI_EPILOG,
                                            add_help = False,
                                            formatter_class=ArgumentDefaultsHelpFormatter)

    system_flags: _ArgumentGroup = parser.add_argument_group("system flags")
    application_flags: _ArgumentGroup = parser.add_argument_group("application flags")
    required: _ArgumentGroup = parser.add_argument_group("required arguments")
    optional: _ArgumentGroup = parser.add_argument_group("optional arguments")

    add_help_flag(system_flags)
    for key, value in system_flag_list.items():
        add_cli_flag(system_flags, key, value)
    for key, value in application_flag_list.items():
        add_cli_flag(application_flags, key, value)

    add_cli_argument(required, "-t", "--targets", str)
    add_cli_argument(required, "-p", "--include-ports", str)

    add_cli_argument(optional, "-b", "--batch-size", int, 0)
    add_cli_argument(optional, "-B", "--batch-delay", int, 60)
    add_cli_argument(optional, "-d", "--delay-time", int, 3)
    add_cli_argument(optional, "-e", "--exclude-port", int)
    add_cli_argument(optional, "-T", "--threads", int, default_threads)
    add_cli_argument(optional, "-f", "--filename", int, "results")

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

    parser: ArgumentParser = __setup_arg_parser()
    args: Namespace = parser.parse_args()

    if args.list_rules is True:
        __list_all_port_rules()
        sys.exit(0)

    if args.include_ports is None or args.targets is None:
        parser.print_help()
        sys.exit(0)

    if args.quiet is True and args.json is False and args.csv is False:
        raise InvalidParameters("[X] Fatal: You cannot use --quiet unless you supply --csv or --json")

    if args.ipv4_only is True and args.ipv6_only is True:
        raise InvalidParameters("[X] Fatal: You cannot use --ipv4_only AND --ipv6_only - pick one!")

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
    except InvalidParameters as e:
        error(str(e))

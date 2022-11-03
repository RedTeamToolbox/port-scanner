#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the summary line

more to follow
"""

import sys

from argparse import Namespace

from modules.cli import process_command_line_arguments
from modules.core import run_scanner
from modules.exceptions import InvalidParameters
from modules.notify import error, info


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

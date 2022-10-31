#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is the summary line

Usage:
    ./port-scan.py [-h] [-q] [-v] [-4] [-6] [-A] [-c] [-j] [-s] [-r] [-t TARGETS] [-b BATCH_SIZE] [-B BATCH_DELAY] [-d DELAY_TIME] [-p INCLUDE_PORTS] [-e EXCLUDE_PORTS] [-T THREADS] [-f FILENAME]


"""

import sys

import modules.cli as PScli
import modules.config as PSconfig
import modules.notify as PSnotify
import modules.outputs as PSoutputs
import modules.ports as PSports
import modules.scanner as PSscanner
import modules.targets as PStargets


def main() -> None:
    """The main function.

    This is the main function for the port scanner. It has been kept intentionally as small as possible and just
    defines the flow of the program.

    1. Get the arguments from the user.
    2. Create the configuration needed.
    3. Scan the targets.
    4. Process the results.
    5. Exit.
    """

    args = PScli.process_command_line_arguments()
    config = PSconfig.build_configuration(args)
    config.ports = PSports.get_target_port_list(args.include_ports, args.exclude_ports)
    config.targets = PStargets.get_target_ip_list(args.targets, args.ipv4_only, args.ipv6_only)
    results = PSscanner.scan_targets(config)
    PSoutputs.display_results(results, config)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        PSnotify.info("[*] Exiting Program")

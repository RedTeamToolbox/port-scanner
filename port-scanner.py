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
import modules.targets as PStargets


def main() -> None:
    """_summary_

    _extended_summary_
    """

    args = PScli.process_arguments()
    config = PSconfig.build_configuration(args, PSports.get_target_port_list, PStargets.get_target_ip_list)
    results = PStargets.scan_targets(config)
    PSoutputs.display_results(results, config)
    sys.exit(0)


if __name__ == "__main__":
    """_summary_

    _extended_summary_
    """
    try:
        main()
    except KeyboardInterrupt:
        PSnotify.info("[*] Exiting Program")

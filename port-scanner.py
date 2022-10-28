#!/usr/bin/env python

"""
stuff



"""

import sys

import modules.cli as PScli
import modules.config as PSconfig
import modules.notify as PSnotify
import modules.outputs as PSoutputs
import modules.targets as PStargets


def main() -> None:
    """
    The main function.
    """

    # Increase the resource limit ??

    args = PScli.process_arguments()
    config = PSconfig.build_configuration(args)
    results = PStargets.scan_targets(config)
    PSoutputs.display_results(results, config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        PSnotify.info("[*] Exiting Program")
        sys.exit(0)

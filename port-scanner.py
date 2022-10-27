#!/usr/bin/env python

"""
stuff

TODO: ip in range a.b.c.d-a.b.c.d
TODO: ip in cidr format a.b.c.d/nn
TODO: ip from filename:
TODO: ports from filename: for both include and exclude
"""

import sys

import modules.cli as PScli
import modules.outputs as PSoutputs
import modules.targets as PStargets


def main() -> None:
    """
    The main function.
    """

    # Increase the resource limit ??

    args = PScli.process_arguments()

    results = PStargets.scan_targets(args)
    PSoutputs.display_results(results, args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[Exiting Program]")
        sys.exit(0)

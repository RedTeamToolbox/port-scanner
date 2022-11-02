# -*- coding: utf-8 -*-
"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

from argparse import Namespace

from .config import build_configuration, Configuration
from .outputs import display_results
from .ports import get_target_port_list
from .scanner import scan_targets
from .targets import get_target_ip_list


def run_scanner(args: Namespace) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        args (argparse.Namespace) -- _description_
    """

    config: Configuration = build_configuration(args)
    config.ports = get_target_port_list(args.include_ports, args.exclude_ports)
    config.targets = get_target_ip_list(args.targets, args.ipv4_only, args.ipv6_only)
    results: list[dict] = scan_targets(config)
    display_results(results, config)

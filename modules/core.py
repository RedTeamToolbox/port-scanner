# -*- coding: utf-8 -*-
"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import argparse
from types import SimpleNamespace

from .config import create_configuration_from_arguments
from .outputs import display_results
from .ports import get_target_port_list
from .scanner import scan_targets
from .targets import get_target_ip_list


def run_scanner(args: argparse.Namespace) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        args (argparse.Namespace) -- _description_
    """
    config: SimpleNamespace = create_configuration_from_arguments(args)
    config.ports = get_target_port_list(args.ports, args.exclude_ports)
    config.targets = get_target_ip_list(args.targets, config.ipv4_only, config.ipv6_only)
    results: list[dict] = scan_targets(config)
    display_results(results, config)

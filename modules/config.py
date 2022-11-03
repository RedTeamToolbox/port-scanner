# -*- coding: utf-8 -*-
"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import argparse

from types import SimpleNamespace


def create_configuration_from_arguments(args: argparse.Namespace) -> SimpleNamespace:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        args (argparse.Namespace) -- _description_

    Returns:
        SimpleNamespace -- _description_
    """
    configuration: SimpleNamespace = SimpleNamespace()

    configuration.quiet = args.quiet
    configuration.verbose = args.verbose
    configuration.debug = args.debug
    configuration.shuffle = args.shuffle
    configuration.ipv4_only = args.ipv4_only
    configuration.ipv6_only = args.ipv6_only
    configuration.all_results = args.all_results
    configuration.batch_size = args.batch_size
    configuration.batch_delay = args.batch_delay
    configuration.delay_time = args.delay_time
    configuration.cache_directory = args.cache_directory
    configuration.filename = args.filename
    configuration.threads = args.threads

    configuration.batched = bool(configuration.batch_size > 0)

    return configuration

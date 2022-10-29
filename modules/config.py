# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import argparse


class Configuration():  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Store configuration

    _extended_summary_
    """

    ports = []
    targets = []
    quiet = False
    verbose = False
    shuffle = True
    ipv4_only = False
    ipv6_only = False
    all_results = False
    csv = False
    json = False
    batch_size = False
    batch_delay = 0
    batched = False
    delay_time = 0
    filename = ''
    threads = 0


def build_configuration(args: argparse.Namespace, get_target_port_list_fn, get_target_ip_list_fn) -> Configuration:
    """_summary_

    _extended_summary_

    Arguments:
        args (argparse.Namespace) -- _description_
        get_target_port_list_fn (_type_) -- _description_
        get_target_ip_list_fn (_type_) -- _description_

    Returns:
        Configuration -- _description_
    """

    config = Configuration()

    config.ports = get_target_port_list_fn(args.include_ports, args.exclude_ports)
    config.targets = get_target_ip_list_fn(args.targets, args.ipv4_only, args.ipv6_only)
    config.quiet = args.quiet
    config.verbose = args.verbose
    config.shuffle = args.shuffle
    config.ipv4_only = args.ipv4_only
    config.ipv6_only = args.ipv6_only
    config.all_results = args.all_results
    config.csv = args.csv
    config.json = args.json
    config.batch_size = args.batch_size
    config.batch_delay = args.batch_delay
    config.delay_time = args.delay_time
    config.filename = args.filename
    config.threads = args.threads

    if config.batch_size:
        config.batched = True
    return config

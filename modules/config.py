"""
Global configuration
"""

import argparse


class Configuration():  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """
    Hold the global configuration
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
    delay = False  # TODO: make this do something
    delay_time = 0  # TODO: make this do something
    filename = ''
    threads = 0


def build_configuration(args: argparse.Namespace, get_target_port_list_fn, get_target_ip_list_fn) -> Configuration:
    """
    Docs
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
    config.delay = args.delay
    config.delay_time = args.delay_time
    config.filename = args.filename
    config.threads = args.threads

    if config.batch_size:
        config.batched = True
    return config

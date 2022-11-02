# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import argparse
from dataclasses import dataclass, field


@dataclass
class Configuration:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """_summary_

    _extended_summary_
    """

    ports: list = field(default_factory=list)
    targets: list = field(default_factory=list)
    quiet: bool = False
    verbose: bool = False
    debug: bool = False
    shuffle: bool = True
    ipv4_only: bool = False
    ipv6_only: bool = False
    all_results: bool = False
    batch_size: int = 3
    batch_delay: int = 0
    batched: bool = False
    delay_time: int = 0
    filename: str = ''
    threads: int = 0


def build_configuration(args: argparse.Namespace) -> Configuration:
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

    config.quiet = args.quiet
    config.verbose = args.verbose
    # config.debug = args.debug
    config.shuffle = args.shuffle
    config.ipv4_only = args.ipv4_only
    config.ipv6_only = args.ipv6_only
    config.all_results = args.all_results
    config.batch_size = args.batch_size
    config.batch_delay = args.batch_delay
    config.delay_time = args.delay_time
    config.filename = args.filename
    config.threads = args.threads

    if config.batch_size:
        config.batched = True
    return config

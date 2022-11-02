# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import ipaddress
import itertools
import socket
import sys

from ipaddress import IPv4Address, IPv6Address
from typing import Any

import dns.resolver

from .globals import host_ip_mapping, ip_ipnum_mapping
from .notify import error, info_msg, warn
from .utils import create_spinner


def is_ip_address(target: str) -> Any:
    """_summary_

    _extended_summary_

    Arguments:
        target (str) -- _description_

    Returns:
        Any -- _description_
    """
    try:
        ip: IPv4Address | IPv6Address = ipaddress.ip_address(target)
        status: bool = bool(isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)))
    except ValueError:
        status = False

    return status


def get_records(host: str, record_type: str) -> list[str]:
    """_summary_

    _extended_summary_

    Arguments:
        host (str) -- _description_
        record_type (str) -- _description_

    Returns:
        list[str] -- _description_
    """
    try:
        resolver_results: list = dns.resolver.resolve(host, record_type)
        results: list = [val.to_text() for val in resolver_results]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        results = []

    return results


def get_ips(target: str, ipv4_only: bool, ipv6_only: bool) -> list[str]:
    """_summary_

    _extended_summary_

    Arguments:
        target (str) -- _description_
        ipv4_only (bool) -- _description_
        ipv6_only (bool) -- _description_

    Returns:
        list[str] -- _description_
    """

    if is_ip_address(target) is False:
        if ipv4_only is True:
            results: list[str] = sorted(get_records(target, "A"))
        elif ipv6_only is True:
            results: list[str] = sorted(get_records(target, "AAAA"))
        else:
            results: list[str] = sorted(get_records(target, "A")) + sorted(get_records(target, "AAAA"))
    else:
        results = [target]
    return results


def validate_targets(targets: list[str], ipv4_only: bool, ipv6_only: bool) -> list[str]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list[str]) -- _description_
        ipv4_only (bool) -- _description_
        ipv6_only (bool) -- _description_

    Returns:
        list[str] -- _description_
    """
    valid_targets: list = []

    for target in targets:
        try:
            for ip in get_ips(target, ipv4_only, ipv6_only):
                if (ip in host_ip_mapping and is_ip_address(target) is False) or ip not in host_ip_mapping:
                    host_ip_mapping[ip] = target
                ip_ipnum_mapping[ip] = int(ipaddress.ip_address(ip))
                valid_targets.append(ip)

        except socket.gaierror:
            warn(f"{target} is not valid - Skipping)")

    # Now we need to remove any duplicates and sort
    valid_targets = sorted(list(set(valid_targets)))
    return valid_targets


# TODO: move this to somewhere else

def get_all_host_port_combinations(targets: list[str], ports: list[int]) -> list[tuple]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list[str]) -- _description_
        ports (list[int]) -- _description_

    Returns:
        list[tuple] -- _description_
    """
    return list(itertools.product(targets, ports))


def get_target_ip_list(targets: str, ipv4_only: bool, ipv6_only: bool) -> list[str]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (str) -- _description_
        ipv4_only (bool) -- _description_
        ipv6_only (bool) -- _description_

    Returns:
        list[str] -- _description_
    """

    with create_spinner(info_msg("[*] Generating a list of all target IP address")):
        target_list: list[str] = targets.split(",")
        valid_targets: list[str] = validate_targets(target_list, ipv4_only, ipv6_only)

    if not valid_targets:
        error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)

    return valid_targets

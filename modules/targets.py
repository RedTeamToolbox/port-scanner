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

from typing import Any

import dns.resolver

import modules.globals as PSglobals
import modules.notify as PSnotify
import modules.utils as PSutils


def is_ip_address(target: str) -> Any:
    """_summary_

    _extended_summary_

    Arguments:
        target (str) -- _description_

    Returns:
        Any -- _description_
    """
    try:
        ip = ipaddress.ip_address(target)
        status = bool(isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)))
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
        resolver_results = dns.resolver.resolve(host, record_type)
        results = [val.to_text() for val in resolver_results]
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
            results = sorted(get_records(target, "A"))
        elif ipv6_only is True:
            results = sorted(get_records(target, "AAAA"))
        else:
            results = sorted(get_records(target, "A")) + sorted(get_records(target, "AAAA"))
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
    valid_targets = []

    for target in targets:
        try:
            for ip in get_ips(target, ipv4_only, ipv6_only):
                if (ip in PSglobals.host_ip_mapping and is_ip_address(target) is False) or ip not in PSglobals.host_ip_mapping:
                    PSglobals.host_ip_mapping[ip] = target
                PSglobals.ip_ipnum_mapping[ip] = int(ipaddress.ip_address(ip))
                valid_targets.append(ip)

        except socket.gaierror:
            PSnotify.warn(f"{target} is not valid - Skipping)")

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

    with PSutils.create_spinner(PSnotify.info_msg("[*] Generating a list of all target IP address")):
        target_list = targets.split(",")
        valid_targets = validate_targets(target_list, ipv4_only, ipv6_only)

    if not valid_targets:
        PSnotify.error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)

    return valid_targets

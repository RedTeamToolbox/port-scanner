# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import ipaddress
import itertools
import os
import re
import socket
import sys

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from re import Match
from types import SimpleNamespace
from typing import Any

import dns.resolver

from .globals import host_ip_mapping, ip_ipnum_mapping
from .notify import error, info_msg, warn
from .utils import create_spinner


def ips_from_range(ip_lower, ip_upper, inclusive=True) -> list[IPv4Address | IPv6Address]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        ip_lower (_type_) -- _description_
        ip_upper (_type_) -- _description_

    Keyword Arguments:
        inclusive (bool) -- _description_ (default: True)

    Returns:
        list[IPv4Address | IPv6Address] -- _description_
    """
    results: list[IPv4Address | IPv6Address] = []

    try:
        lower: int = int(ipaddress.ip_address(ip_lower))
        upper: int = int(ipaddress.ip_address(ip_upper))
    except ValueError:
        # TODO: Raise an exception
        return []

    if inclusive is True:
        upper += 1

    for i in range(lower, upper):
        results.append(ipaddress.ip_address(i))

    return results


def ips_from_cidr(ip_address, hosts_only=False) -> list[IPv4Address | IPv6Address]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        ip_address (_type_) -- _description_

    Keyword Arguments:
        hosts_only (bool) -- _description_ (default: False)

    Returns:
        list[IPv4Address | IPv6Address] -- _description_
    """
    results: list[IPv4Address | IPv6Address] = []

    try:
        net: IPv4Network | IPv6Network = ipaddress.ip_network(ip_address, strict=False)
    except (ipaddress.NetmaskValueError, ipaddress.AddressValueError):
        # TODO: Raise an exception
        return []

    if hosts_only is True:
        results = list(net.hosts())
    else:
        results = list(net)

    return results


# TODO: define internal functions
def is_ip_address(target: str) -> Any:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        target (str) -- _description_

    Returns:
        Any -- _description_
    """
    try:
        ip_address: IPv4Address | IPv6Address = ipaddress.ip_address(target)
        status: bool = bool(isinstance(ip_address, (ipaddress.IPv4Address, ipaddress.IPv6Address)))
    except ValueError:
        status = False

    return status


def get_records(host: str, record_type: str) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

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
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        target (str) -- _description_
        ipv4_only (bool) -- _description_
        ipv6_only (bool) -- _description_

    Returns:
        list[str] -- _description_
    """
    results: list[str] = []

    if is_ip_address(target) is False:
        if ipv4_only is True:
            results = sorted(get_records(target, "A"))
        elif ipv6_only is True:
            results = sorted(get_records(target, "AAAA"))
        else:
            results = sorted(get_records(target, "A")) + sorted(get_records(target, "AAAA"))
    else:
        results.append(target)

    return results


def store_host_ip_mapping(target: str, ip_address: str) -> bool:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        target (str) -- _description_
        ip_address (str) -- _description_

    Returns:
        bool -- _description_
    """
    if ip_address in host_ip_mapping and is_ip_address(target) is False:
        return True
    if ip_address not in host_ip_mapping:
        return True
    return False


def validate_targets(targets: list[str], ipv4_only: bool, ipv6_only: bool) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

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
            for ip_address in get_ips(target, ipv4_only, ipv6_only):
                if (ip_address in host_ip_mapping and is_ip_address(target) is False) or ip_address not in host_ip_mapping:
                    host_ip_mapping[ip_address] = target

                ipnum: int = int(ipaddress.ip_address(ip_address))
                ip_ipnum_mapping[ip_address] = ipnum
                valid_targets.append(ip_address)

        except socket.gaierror:
            warn(f"{target} is not valid - Skipping)")

    # Now we need to remove any duplicates and sort
    valid_targets = sorted(list(set(valid_targets)))
    return valid_targets


# TODO: move this to somewhere else

def get_all_host_port_combinations(targets: list[str], ports: list[int]) -> list[tuple]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (list[str]) -- _description_
        ports (list[int]) -- _description_

    Returns:
        list[tuple] -- _description_
    """
    return list(itertools.product(targets, ports))


def _update_host_mappings(targets: list[IPv4Address | IPv6Address]) -> None:

    for ip_address in targets:
        ip_str: str = str(ip_address)

        host_ip_mapping[ip_str] = ip_str
        ip_ipnum_mapping[ip_str] = int(ip_address)


def _get_target_from_name(target: str, config: SimpleNamespace) -> list[str]:
    results: list[str] = []

    try:
        for ip_address in get_ips(target, config.ipv4_only, config.ipv6_only):
            # Prefer the hostname (if given) over the IP address
            if (ip_address in host_ip_mapping and is_ip_address(target) is False) or ip_address not in host_ip_mapping:
                host_ip_mapping[ip_address] = target

            ip_ipnum_mapping[ip_address] = int(ipaddress.ip_address(ip_address))
            results.append(ip_address)

    except socket.gaierror:
        warn(f"{target} is not valid - Skipping)")

    return results


def _get_targets_from_cidr(target: str, _config: SimpleNamespace) -> list[str]:
    ip_results: list[IPv4Address | IPv6Address] = []
    results: list[str] = []

    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)", target):
        ip_results = ips_from_cidr(target)
        _update_host_mappings(ip_results)
        results = [str(ip_address) for ip_address in ip_results]

    return results


def _get_targets_from_range(target: str, _config: SimpleNamespace) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ip_results: list[IPv4Address | IPv6Address] = []
    results: list[str] = []

    match_result: Match[str] | None = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[-:](\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", target)
    if match_result is not None:
        ip_results = ips_from_range(match_result.group(1), match_result.group(2))
        _update_host_mappings(ip_results)
        results = [str(ip_address) for ip_address in ip_results]

    return results


def _real_get_target_list(supplied_target_list: str, config: SimpleNamespace) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    # This is order is important as once a port parameter is processed the loop is broken out of.
    functions_to_call: list = [
        _get_targets_from_range,
        _get_targets_from_cidr,
        _get_target_from_name,
    ]
    results: list[str] = []

    for target in supplied_target_list.split(","):
        for func in functions_to_call:
            target_list: list[str] = func(target, config)
            if target_list:
                results += target_list
                break

    # Now we need to remove any duplicates and sort
    results = sorted(list(set(results)))

    return results


def _get_target_list_from_file(target: str) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[str] -- _description_
    """
    targets: list[str] = []

    match_results: Match[str] | None = re.search(r"file:(.*)", target, re.IGNORECASE)
    if match_results is not None:
        fname: str = match_results.group(1)

        if not os.path.exists(fname):
            warn(f"{fname} does not exist - aborting")
        else:
            with open(fname, "r", encoding="UTF-8") as readfile:
                lines: list[str] = readfile.readlines()
                for line in lines:
                    for item in line.strip().split(","):
                        targets.append(item)
    return targets


def _get_target_list(supplied_target_list: str, config: SimpleNamespace) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    results: list[str] = []
    generated_target_list: list[str] = []

    # target_list: list[str] = supplied_target_list.split(",")
    # valid_targets: list[str] = validate_targets(target_list, config.ipv4_only, config.ipv6_only)

    for target in supplied_target_list.split(","):
        target_list: list[str] = _get_target_list_from_file(target)
        if target_list:
            generated_target_list += target_list
        else:
            generated_target_list.append(target)

    results = _real_get_target_list(",".join(generated_target_list), config)

    return results


def get_target_ip_list(include_targets: str, exclude_targets: str, config: SimpleNamespace) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (str) -- _description_
        ipv4_only (bool) -- _description_
        ipv6_only (bool) -- _description_

    Returns:
        list[str] -- _description_
    """
    include_target_list: list[str] = []
    exclude_target_list: list[str] = []
    target_list: list[str] = []

    with create_spinner(info_msg("[*] Generating a list of all target IP address")):
        include_target_list = _get_target_list(include_targets, config)
        if exclude_targets is not None:
            exclude_target_list = _get_target_list(exclude_targets, config)
            if exclude_target_list:
                target_list = [x for x in include_target_list if x not in exclude_target_list]
        else:
            target_list = include_target_list

    if not target_list:
        # TODO: raise an exception
        error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)

    return target_list

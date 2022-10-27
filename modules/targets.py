"""
Docs
"""
import ipaddress
import itertools
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed

from typing import Any

import dns.resolver
import colored
from colored import stylize
from yaspin import yaspin

import modules.globals as PSglobals
import modules.scanner as PSscanner
import modules.utils as PSutils

# TODO: ip in range a.b.c.d-a.b.c.d
# TODO: ip in cidr format a.b.c.d/nn
# TODO: ip from filename:


def is_ip_address(target: str) -> Any:
    """
    docs
    """
    try:
        ip = ipaddress.ip_address(target)
        status = bool(isinstance(ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)))
    except ValueError:
        status = False

    return status


def get_records(host, record_type):
    """
    docs
    """
    try:
        resolver_results = dns.resolver.resolve(host, record_type)
        results = [val.to_text() for val in resolver_results]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        results = []

    return results


def get_ips(target, ipv4_only, ipv6_only):
    """
    docs
    """

    if is_ip_address(target) is False:
        if ipv4_only is True:
            results = sorted(get_records(target, 'A'))
        elif ipv6_only is True:
            results = sorted(get_records(target, 'AAAA'))
        else:
            results = sorted(get_records(target, 'A')) + sorted(get_records(target, 'AAAA'))
    else:
        results = [target]
    return results


def validate_targets(targets, ipv4_only, ipv6_only):
    """
    docs
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
            print(stylize(f"{target} is not valid - Skipping)", colored.fg("yellow")))

    # Now we need to remove any duplicates and sort
    valid_targets = sorted(list(set(valid_targets)))
    return valid_targets


def get_all_host_port_combinations(targets, ports):
    """
    docs
    """
    return list(itertools.product(targets, ports))


def scan_targets(args) -> list:
    """
    Docs
    """
    results = []

    # Take all the ips and ports and get ALL combinations
    with yaspin(text=stylize("Generating all host:port combinations", colored.fg("green")), timer=True) as spinner:
        targets = get_all_host_port_combinations(args.targets, args.include_ports)
        if args.shuffle is True:
            targets = PSutils.shuffled(targets)
    spinner.ok("✅")

    if args.threads > len(targets):
        how_many = len(targets)
    else:
        how_many = args.threads

    with yaspin(text=stylize(f"Processing host port ({how_many} threads)", colored.fg("green")), timer=True) as spinner:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            futures = [executor.submit(PSscanner.scan_target_port, target[0], target[1], spinner, args) for target in targets]

            for future in as_completed(futures):
                thread_results = future.result()
                if thread_results:
                    results.append(thread_results)

    spinner.ok("✅")
    return results

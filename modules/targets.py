"""
Docs
"""
import argparse
import ipaddress
import itertools
import socket
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed

from typing import Any, Type

import dns.resolver
import colored
from colored import stylize
from yaspin import yaspin

import modules.config as PSconfig
import modules.globals as PSglobals
import modules.notify as PSnotify
import modules.scanner as PSscanner
import modules.utils as PSutils

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


# TODO: move this to somewhere else

def get_all_host_port_combinations(targets, ports):
    """
    docs
    """
    return list(itertools.product(targets, ports))

#
# TODO: Move this to the scanner this is the wrong place
#
def scan_targets(config: PSconfig.Configuration) -> list:
    """
    Docs
    """
    results = []

    # Take all the ips and ports and get ALL combinations
    PSnotify.info("[*] Generating all host / port combinations")
    targets = get_all_host_port_combinations(config.targets, config.ports)
    if config.shuffle is True:
        targets = PSutils.shuffled(targets)
    
    if config.threads > len(targets):
        how_many = len(targets)
    else:
        how_many = config.threads

    with PSutils.create_bar(f"Scanning Hosts with {how_many} threads", len(targets)) as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            futures = [executor.submit(PSscanner.scan_target_port, target[0], target[1]) for target in targets]

            for future in as_completed(futures):
                pbar.update(1)
                thread_results = future.result()
                if thread_results:
                    if config.verbose:
                        verbose_msg = f"{thread_results['target']} port {thread_results['port']} is {thread_results['status_string']}"
                        if thread_results['status'] == True:
                            pbar.write(PSnotify.error_msg(f"[X] {verbose_msg}"))
                        else:
                            pbar.write(PSnotify.success_msg(f"[^] {verbose_msg}"))
                    results.append(thread_results)

    return results


def get_target_ip_list(targets: str, ipv4_only: bool, ipv6_only: bool) -> list[str]:
    """
    Docs
    """

    with yaspin(text=PSnotify.info_msg("[*] Generating a list of all target IP address"), timer=True) as spinner:
        target_list = targets.split(',')
        valid_targets = validate_targets(target_list, ipv4_only, ipv6_only)
    spinner.stop()

    if not valid_targets:
        PSnotify.error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)

    return valid_targets
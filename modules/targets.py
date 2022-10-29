# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
import ipaddress
import itertools
import math
import socket
import sys

from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from typing import Any

import dns.resolver
import colored
from colored import stylize
from yaspin import yaspin

import modules.config as PSconfig
import modules.globals as PSglobals
import modules.notify as PSnotify
import modules.scanner as PSscanner
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
            print(stylize(f"{target} is not valid - Skipping)", colored.fg("yellow")))

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


def handle_verbose_mode(thread_results: dict, pbar) -> None:
    """_summary_

    Args:
        thread_results (dict): _description_
        pbar (_type_): _description_
    """

    verbose_msg = f"{thread_results['target']} port {thread_results['port']} is {thread_results['status_string']}"
    if thread_results['status'] is True:
        pbar.write(PSnotify.error_msg(f"[X] {verbose_msg}"))
    else:
        pbar.write(PSnotify.success_msg(f"[^] {verbose_msg}"))


def get_how_many(targets: list, config: PSconfig.Configuration) -> int:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        int -- _description_
    """

    if config.threads > len(targets):
        how_many = len(targets)
    else:
        how_many = config.threads

    return how_many


def scan_targets_batched(targets: list, how_many: int, config: PSconfig.Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """
    results = []

    number_of_batches = math.ceil(len(targets) / config.batch_size)
    PSnotify.info(f"[+] We will execute the scans in {number_of_batches} batches with {config.batch_size} scan per batch")
    batches = [targets[i * config.batch_size:(i + 1) * config.batch_size] for i in range((len(targets) + config.batch_size - 1) // config.batch_size)]

    if how_many > config.batch_size:
        how_many = config.batch_size

    batch_counter = 0

    with PSutils.create_bar("Total", len(targets)) as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            with PSutils.create_bar("Batches", number_of_batches, leave = False) as pbar_batches:
                for batch in batches:
                    batch_counter += 1
                    with PSutils.create_bar(f"Batches {batch_counter}", config.batch_size, leave = False) as batches:
                        futures = [executor.submit(PSscanner.scan_target_port, target[0], target[1], config.delay_time) for target in batch]

                        for future in as_completed(futures):
                            pbar.update(1)
                            batches.update(1)
                            thread_results = future.result()
                            if thread_results:
                                results.append(thread_results)
                                if config.verbose is True:
                                    handle_verbose_mode(thread_results, pbar)

                    pbar_batches.update(1)
                    sleep(config.batch_delay)
    return results


def scan_targets_unbatched(targets: list, how_many: int, config: PSconfig.Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """
    results = []

    with PSutils.create_bar(f"{len(targets)} scans with {how_many} threads", len(targets)) as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            futures = [executor.submit(PSscanner.scan_target_port, target[0], target[1], config.delay_time) for target in targets]

            for future in as_completed(futures):
                pbar.update(1)
                thread_results = future.result()
                if thread_results:
                    results.append(thread_results)
                    if config.verbose is True:
                        handle_verbose_mode(thread_results, pbar)
    return results


def scan_targets(config: PSconfig.Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """
    # Take all the ips and ports and get ALL combinations
    PSnotify.info("[*] Generating all host / port combinations")
    targets = get_all_host_port_combinations(config.targets, config.ports)
    if config.shuffle is True:
        targets = PSutils.shuffled(targets)

    how_many = get_how_many(targets, config)

    if config.batched:
        return scan_targets_batched(targets, how_many, config)
    return scan_targets_unbatched(targets, how_many, config)


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

    with yaspin(text=PSnotify.info_msg("[*] Generating a list of all target IP address"), timer=True) as spinner:
        target_list = targets.split(",")
        valid_targets = validate_targets(target_list, ipv4_only, ipv6_only)
    spinner.stop()

    if not valid_targets:
        PSnotify.error("Fatal: No valid targets were found - Aborting!")
        sys.exit(0)
    return valid_targets

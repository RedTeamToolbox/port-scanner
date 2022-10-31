# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import ipaddress
import math
import re
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from typing import Any

import modules.config as PSconfig
import modules.globals as PSglobals
import modules.notify as PSnotify
import modules.ordering as PSordering
import modules.targets as PStargets
import modules.utils as PSutils


def scan_target_port(target: str, port: int, delay_time: int) -> dict[str, Any]:
    """_summary_

    _extended_summary_

    Arguments:
        target (str) -- _description_
        port (int) -- _description_
        delay_time (int) -- _description_

    Returns:
        dict[str, Any] -- _description_
    """
    status = False
    status_string = "Closed"
    error_msg = None
    banner = None

    if delay_time > 0:
        sleep(delay_time)

    ip = ipaddress.ip_address(target)
    if isinstance(ip, ipaddress.IPv6Address) is True:
        af_type = socket.AF_INET6
    else:
        af_type = socket.AF_INET

    with socket.socket(af_type, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((target, port))
            # sock.settimeout(3)
            status_string = "Open"
            status = True
            try:
                banner = sock.recv(2048).decode("utf-8").strip()
            except socket.error as err:
                banner = "Unavailable"
                error_msg = err
            sock.shutdown(0)
            sock.close()
        except socket.timeout:
            error_msg = "Connection timed out"
            status_string = "Closed"
            status = False
        except socket.error as err:
            error_msg = str(err)
            result = re.search(r"(\[Errno \d+\] )?(.*)", error_msg)
            if result is not None:
                error_msg = result.group(2)
            status_string = "Closed"
            status = False

    # Cache the service name in case we are hitting multiple IPs
    if port not in PSglobals.service_name_mapping:
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"
        PSglobals.service_name_mapping[port] = service

    return {
            "target": PSglobals.host_ip_mapping[target],
            "ip": ip,
            "ipnum": PSglobals.ip_ipnum_mapping[target],
            "port": port,
            "status": status,
            "status_string": status_string,
            "service": PSglobals.service_name_mapping[port],
            "banner": banner,
            "error": error_msg
           }


def handle_verbose_mode(thread_results: dict) -> None:
    """_summary_

    Args:
        thread_results (dict): _description_
        pbar (_type_): _description_
    """

    verbose_msg = f"{thread_results['target']} port {thread_results['port']} is {thread_results['status_string']}"
    if thread_results['status'] is True:
        print(PSnotify.error_msg(f"[X] {verbose_msg}"))
    else:
        print(PSnotify.success_msg(f"[^] {verbose_msg}"))


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

    with PSutils.create_alive_bar(len(targets), title=f"{len(targets)} scans with {how_many} threads") as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            for batch in batches:
                pbar.text = PSnotify.info_msg("Status: Submitting jobs for batch {batch_counter}")
                batch_counter += 1

                futures = [executor.submit(scan_target_port, target[0], target[1], config.delay_time) for target in batch]
                pbar.text = PSnotify.info_msg(f"Status: Batch {batch_counter} jobs submitted - awaiting results")

                for future in as_completed(futures):
                    pbar.text = PSnotify.info_msg(f"Status: Processing results for batch {batch_counter}")
                    pbar()  # pylint: disable=not-callable
                    thread_results = future.result()
                    if thread_results:
                        results.append(thread_results)
                        if config.verbose is True:
                            handle_verbose_mode(thread_results)

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

    with PSutils.create_alive_bar(len(targets), title=f"{len(targets)} scans with {how_many} threads") as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            pbar.text = PSnotify.info_msg("Status: Submitting jobs")
            futures = [executor.submit(scan_target_port, target[0], target[1], config.delay_time) for target in targets]
            pbar.text = PSnotify.info_msg("Status: Jobs submitted - awaiting results")

            for future in as_completed(futures):
                pbar()  # pylint: disable=not-callable
                pbar.text = PSnotify.info_msg("Status: Processing results")
                thread_results = future.result()
                if thread_results:
                    results.append(thread_results)
                    if config.verbose is True:
                        handle_verbose_mode(thread_results)
    return results


def scan_targets(config: PSconfig.Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """

    with PSutils.create_spinner(PSnotify.info_msg("[*] Generating all host / port combinations")):
        targets = PStargets.get_all_host_port_combinations(config.targets, config.ports)
        if config.shuffle is True:
            targets = PSordering.shuffled(targets)

    how_many = get_how_many(targets, config)

    if config.batched:
        return scan_targets_batched(targets, how_many, config)
    return scan_targets_unbatched(targets, how_many, config)

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
from ipaddress import IPv4Address, IPv6Address
from re import Match
from time import sleep
from typing import Any

from .config import Configuration
from .globals import host_ip_mapping, ip_ipnum_mapping, service_name_mapping
from .notify import error_msg, info_msg, success_msg, info
from .ordering import shuffled
from .targets import get_all_host_port_combinations
from .utils import create_alive_bar, create_spinner


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
    status: bool = False
    status_string: str = "Closed"
    error_from_server: str = ""
    banner: str = ""

    if delay_time > 0:
        sleep(delay_time)

    ip: IPv4Address | IPv6Address = ipaddress.ip_address(target)
    if isinstance(ip, ipaddress.IPv6Address) is True:
        af_type: int = socket.AF_INET6
    else:
        af_type: int = socket.AF_INET

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
                error_from_server = str(err)
            sock.shutdown(0)
            sock.close()
        except socket.timeout:
            error_from_server = "Connection timed out"
            status_string = "Closed"
            status = False
        except socket.error as err:
            error_from_server = str(err)
            result: Match[str] | None = re.search(r"(\[Errno \d+\] )?(.*)", error_from_server)
            if result is not None:
                error_from_server = result.group(2)
            status_string = "Closed"
            status = False

    # Cache the service name in case we are hitting multiple IPs
    if port not in service_name_mapping:
        try:
            service: str = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"
        service_name_mapping[port] = service

    return {
            "target": host_ip_mapping[target],
            "ip": ip,
            "ipnum": ip_ipnum_mapping[target],
            "port": port,
            "status": status,
            "status_string": status_string,
            "service": service_name_mapping[port],
            "banner": banner,
            "error": error_from_server
           }


def handle_verbose_mode(thread_results: dict) -> None:
    """_summary_

    Args:
        thread_results (dict): _description_
        pbar (_type_): _description_
    """

    verbose_msg: str = f"{thread_results['target']} port {thread_results['port']} is {thread_results['status_string']}"
    if thread_results['status'] is True:
        print(error_msg(f"[X] {verbose_msg}"))
    else:
        print(success_msg(f"[^] {verbose_msg}"))


def get_how_many(targets: list, config: Configuration) -> int:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        int -- _description_
    """

    if config.threads > len(targets):
        how_many: int = len(targets)
    else:
        how_many: int = config.threads

    return how_many


def scan_targets_batched(targets: list, how_many: int, config: Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """
    results: list = []

    number_of_batches: int = math.ceil(len(targets) / config.batch_size)
    info(f"[+] We will execute the scans in {number_of_batches} batches with {config.batch_size} scan per batch")
    batches: list = [targets[i * config.batch_size:(i + 1) * config.batch_size] for i in range((len(targets) + config.batch_size - 1) // config.batch_size)]

    workers: int = how_many
    if workers > config.batch_size:
        workers = config.batch_size

    batch_counter: int = 0

    with create_alive_bar(len(targets), title=f"{len(targets)} scans with {workers} threads") as pbar:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for batch in batches:
                pbar.text = info_msg("Status: Submitting jobs for batch {batch_counter}")
                batch_counter += 1

                futures: list = [executor.submit(scan_target_port, target[0], target[1], config.delay_time) for target in batch]
                pbar.text = info_msg(f"Status: Batch {batch_counter} jobs submitted - awaiting results")

                for future in as_completed(futures):
                    pbar.text = info_msg(f"Status: Processing results for batch {batch_counter}")
                    pbar()  # pylint: disable=not-callable
                    thread_results: dict = future.result()
                    if thread_results:
                        results.append(thread_results)
                        if config.verbose is True:
                            handle_verbose_mode(thread_results)

                sleep(config.batch_delay)
    return results


def scan_targets_unbatched(targets: list, how_many: int, config: Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """
    results: list = []

    with create_alive_bar(len(targets), title=f"{len(targets)} scans with {how_many} threads") as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            pbar.text = info_msg("Status: Submitting jobs")
            futures: list = [executor.submit(scan_target_port, target[0], target[1], config.delay_time) for target in targets]
            pbar.text = info_msg("Status: Jobs submitted - awaiting results")

            for future in as_completed(futures):
                pbar()  # pylint: disable=not-callable
                pbar.text = info_msg("Status: Processing results")
                thread_results: dict = future.result()
                if thread_results:
                    results.append(thread_results)
                    if config.verbose is True:
                        handle_verbose_mode(thread_results)
    return results


def scan_targets(config: Configuration) -> list[dict]:
    """_summary_

    _extended_summary_

    Arguments:
        config (PSconfig.Configuration) -- _description_

    Returns:
        list[dict] -- _description_
    """

    with create_spinner(info_msg("[*] Generating all host / port combinations")):
        targets: list[tuple] = get_all_host_port_combinations(config.targets, config.ports)
        if config.shuffle is True:
            targets = shuffled(targets)

    how_many: int = get_how_many(targets, config)

    if config.batched:
        return scan_targets_batched(targets, how_many, config)
    return scan_targets_unbatched(targets, how_many, config)

# -*- coding: utf-8 -*-

"""This is the summary line.

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
from ipaddress import IPv6Address
from re import Match
from time import sleep
from types import SimpleNamespace
from typing import Any

from .globals import host_ip_mapping, ip_ipnum_mapping, service_name_mapping
from .notify import error_msg, info_msg, success_msg, info
from .ordering import shuffled
from .targets import get_all_host_port_combinations
from .utils import create_alive_bar, create_spinner


def add_to_service_mapping(port: int) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (int) -- _description_
    """
    if port not in service_name_mapping:
        try:
            service: str = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"
        service_name_mapping[port] = service


# TODO: define internal functions
def scan_target_port(target: str, port: int, socket_timeout: int, delay_time: int) -> dict[str, Any]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        target (str) -- _description_
        port (int) -- _description_
        delay_time (int) -- _description_

    Returns:
        dict[str, Any] -- _description_
    """
    status: bool = False
    error_from_server: str = ""
    banner: str = ""
    af_type: int = socket.AF_INET

    if delay_time > 0:
        sleep(delay_time)

    if isinstance(ipaddress.ip_address(target), IPv6Address) is True:
        af_type = socket.AF_INET6

    with socket.socket(af_type, socket.SOCK_STREAM) as sock:
        sock.settimeout(socket_timeout)
        try:
            sock.connect((target, port))
            status = True
            try:
                banner = sock.recv(2048).decode("utf-8").strip()
            except socket.error as err:
                error_from_server = str(err)
            sock.shutdown(0)
            sock.close()
        except socket.timeout:
            error_from_server = "Connection timed out"
            status = False
        except socket.error as err:
            error_from_server = str(err)
            result: Match[str] | None = re.search(r"(\[Errno \d+\] )?(.*)", error_from_server)
            if result is not None:
                error_from_server = result.group(2)
            status = False

    # Cache the service name in case we are hitting multiple IPs
    add_to_service_mapping(port)

    status_string: str = "Open" if status is True else "Closed"

    return {
        "target": host_ip_mapping[target],
        "ip": target,
        "ipnum": ip_ipnum_mapping[target],
        "port": port,
        "status": status,
        "status_string": status_string,
        "service": service_name_mapping[port],
        "banner": banner,
        "error": error_from_server
    }


def handle_verbose_mode(thread_results: dict) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        thread_results (dict) -- _description_
    """
    verbose_msg: str = f"{thread_results['target']} port {thread_results['port']} is {thread_results['status_string']}"

    if thread_results['status'] is True:
        print(error_msg(f"[X] {verbose_msg}"))
    else:
        print(success_msg(f"[^] {verbose_msg}"))


def get_how_many(config: SimpleNamespace) -> int:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (list) -- _description_
        args (_type_) -- _description_

    Returns:
        int -- _description_
    """
    how_many: int = config.threads

    if config.threads > len(config.targets):
        how_many = len(config.targets)

    return how_many


def scan_targets_batched(targets: list, how_many: int, config: SimpleNamespace) -> list[dict]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        args (_type_) -- _description_

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

                futures: list = [executor.submit(scan_target_port, target[0], target[1], config.socket_timeout, config.delay_time) for target in batch]
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


def scan_targets_unbatched(targets: list, how_many: int, config: SimpleNamespace) -> list[dict]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (list) -- _description_
        how_many (int) -- _description_
        args (_type_) -- _description_

    Returns:
        list[dict] -- _description_
    """
    results: list = []

    with create_alive_bar(len(targets), title=f"{len(targets)} scans with {how_many} threads") as pbar:
        with ThreadPoolExecutor(max_workers=how_many) as executor:
            pbar.text = info_msg("Status: Submitting jobs")
            futures: list = [executor.submit(scan_target_port, target[0], target[1], config.socket_timeout, config.delay_time) for target in targets]
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


def scan_targets(config: SimpleNamespace) -> list[dict]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        targets (list[str]) -- _description_
        ports (list[int]) -- _description_
        args (_type_) -- _description_

    Returns:
        list[dict] -- _description_
    """
    with create_spinner(info_msg("[*] Generating all host / port combinations")):
        targets_and_ports: list[tuple] = get_all_host_port_combinations(config.targets, config.ports)
        if config.shuffle is True:
            targets_and_ports = shuffled(targets_and_ports)

    how_many: int = get_how_many(config)

    if config.batched:
        return scan_targets_batched(targets_and_ports, how_many, config)
    return scan_targets_unbatched(targets_and_ports, how_many, config)

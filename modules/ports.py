# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import os.path
import re
import socket
import sys

from re import Match

from .constants import PORT_RULES
from .notify import error, info, info_msg, warn
from .utils import create_spinner


def list_all_port_rules() -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.
    """
    info("Available rule sets:")
    count: int = 0
    for rule in PORT_RULES:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


def _get_ports_by_name(port: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports: list = []

    try:
        ports.append(socket.getservbyname(port))
    except OSError:
        warn(f"{port} is not a valid service name - Skipping!")
    return ports


def _get_ports_by_number(port: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports: list = []

    if port.isnumeric():
        ports.append(int(port))
    return ports


def _get_ports_from_rule(rule_name: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        rule_name (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    for rule in PORT_RULES:
        if rule['rule'] == rule_name:
            return rule['ports']

    warn(f"{rule_name} is not a valid ruleset - Skipping!")
    return []


def _get_ports_from_rule_sets(port: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports: list = []

    match_results: Match[str] | None = re.search(r"ruleset:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        rule_sets: str = match_results.group(1)
        for rule in rule_sets.split(","):
            ports += _get_ports_from_rule(rule)
    return ports


def _get_ports_from_range(port: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    result: Match[str] | None = re.search(r"(\d+)[-:](\d+)", port)
    if result is not None:
        return list(range(int(result.group(1)), int(result.group(2)) + 1))

    return []


def _get_port_list_from_file(port: str) -> list[str]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        port (str) -- _description_

    Returns:
        list[str] -- _description_
    """
    ports: list = []

    match_results: Match[str] | None = re.search(r"file:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        fname: str = match_results.group(1)

        if not os.path.exists(fname):
            warn(f"{fname} does not exist - aborting")
        else:
            with open(fname, "r", encoding="UTF-8") as readfile:
                lines: list[str] = readfile.readlines()
                for line in lines:
                    for item in line.strip().split(","):
                        ports.append(item)
    return ports


def real_get_port_list(supplied_port_list: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    # This is order is important as once a port parameter is processed the loop is broken out of.
    functions_to_call: list = [
        _get_ports_from_range,
        _get_ports_from_rule_sets,
        _get_ports_by_number,
        _get_ports_by_name
    ]
    generate_post_ports: list = []

    for port in supplied_port_list.split(","):
        for func in functions_to_call:
            port_list: list[int] = func(port)
            if port_list:
                generate_post_ports += port_list
                break

    # Now we need to remove any duplicates and sort
    generate_post_ports = sorted(list(set(generate_post_ports)))

    return generate_post_ports


def _get_port_list(supplied_port_list: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    # If there is a filename we need to pull the lists out of the file first!
    generated_port_list: list = []

    for port in supplied_port_list.split(","):
        port_list: list[str] = _get_port_list_from_file(port)
        if port_list:
            generated_port_list += port_list
        else:
            generated_port_list.append(port)

    return real_get_port_list(",".join(generated_port_list))


def get_target_port_list(include_ports: str, exclude_ports: str) -> list[int]:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        include_ports (str) -- _description_
        exclude_ports (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    include_port_list: list = []
    exclude_port_list: list = []
    port_list: list = []

    with create_spinner(info_msg("[*] Processing target port list")):
        include_port_list = _get_port_list(include_ports)
        if exclude_ports is not None:
            exclude_port_list = _get_port_list(exclude_ports)
            if exclude_port_list:
                port_list = [x for x in include_port_list if x not in exclude_port_list]
        else:
            port_list = include_port_list

    if not port_list:
        # TODO : raise an exception
        error("Fatal: No valid ports were found - Aborting!")
        sys.exit(0)

    return port_list

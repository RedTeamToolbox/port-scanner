# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import os.path
import re
import socket
import sys

import modules.constants as PSconstants
import modules.notify as PSnotify
import modules.utils as PSutils


def __get_ports_by_name(port: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports = []

    try:
        ports.append(socket.getservbyname(port))
    except OSError:
        PSnotify.warn(f"{port} is not a valid service name - Skipping!")
    return ports


def __get_ports_by_number(port: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports = []

    if port.isnumeric():
        ports.append(int(port))
    return ports


def __get_ports_from_rule(rule_name: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        rule_name (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    for rule in PSconstants.PORT_RULES:
        if rule['rule'] == rule_name:
            return rule['ports']
    PSnotify.warn(f"{rule_name} is not a valid ruleset - Skipping!")
    return []


def __get_ports_from_rule_sets(port: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    ports = []

    match_results = re.search(r"ruleset:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        rule_sets = match_results.group(1)
        for rule in rule_sets.split(","):
            ports += __get_ports_from_rule(rule)
    return ports


def __get_ports_from_range(port: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        port (str) -- _description_

    Returns:
        list[int] -- _description_
    """

    # Format A-B e.g. 1-1024
    result = re.search(r"(\d+)-(\d+)", port)
    if result is not None:
        return list(range(int(result.group(1)), int(result.group(2)) + 1))

    # Format A:B e.g.
    result = re.search(r"(\d+):(\d+)", port)
    if result is not None:
        return list(range(int(result.group(1)), int(result.group(2)) + 1))

    return []


def __get_port_list_from_file(port: str) -> list[str]:
    """_summary_

    _extended_summary_

    Arguments:
        port (str) -- _description_

    Returns:
        list[str] -- _description_
    """
    ports = []

    match_results = re.search(r"file:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        fname = match_results.group(1)

        if not os.path.exists(fname):
            PSnotify.warn(f"{fname} does not exist - aborting")
        else:
            with open(fname, "r", encoding="UTF-8") as f:
                lines = f.readlines()
                for line in lines:
                    for item in line.strip().split(","):
                        ports.append(item)
    return ports


def real_get_port_list(supplied_port_list: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    # This is order is important as once a port parameter is processed the loop is broken out of.
    functions_to_call = [__get_ports_from_range, __get_ports_from_rule_sets, __get_ports_by_number, __get_ports_by_name]
    generate_post_ports = []

    for port in supplied_port_list.split(","):
        for func in functions_to_call:
            port_list = func(port)
            if port_list:
                generate_post_ports += port_list
                break

    # Now we need to remove any duplicates and sort
    generate_post_ports = sorted(list(set(generate_post_ports)))

    return generate_post_ports


def __get_port_list(supplied_port_list: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        supplied_port_list (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    # If there is a filename we need to pull the lists out of the file first!
    generated_port_list = []

    for port in supplied_port_list.split(","):
        port_list = __get_port_list_from_file(port)
        if port_list:
            generated_port_list += port_list
        else:
            generated_port_list.append(port)

    return real_get_port_list(",".join(generated_port_list))


def get_target_port_list(include_ports: str, exclude_ports: str) -> list[int]:
    """_summary_

    _extended_summary_

    Arguments:
        include_ports (str) -- _description_
        exclude_ports (str) -- _description_

    Returns:
        list[int] -- _description_
    """
    include_port_list = []
    exclude_port_list = []
    port_list = []

    with PSutils.create_spinner(PSnotify.info_msg("[*] Processing target port list")):
        include_port_list = __get_port_list(include_ports)
        if exclude_ports is not None:
            exclude_port_list = __get_port_list(exclude_ports)
            if exclude_port_list:
                port_list = [x for x in include_port_list if x not in exclude_port_list]
        else:
            port_list = include_port_list

    if not port_list:
        PSnotify.error("Fatal: No valid ports were found - Aborting!")
        sys.exit(0)

    return port_list

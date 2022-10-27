"""
Docs
"""

from fileinput import filename
import os.path
import re
import socket

import colored
from colored import stylize

import modules.constants as PSconstants
import modules.notify as PSnotify


def list_all_port_rules() -> None:
    """
    Docs
    """

    print(stylize("Available rule sets:", colored.fg("cyan")))
    count = 0
    for rule in PSconstants.PORT_RULES:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


def get_ports_by_name(port: str) -> list[int]:
    """
    Docs
    """
    ports = []

    try:
        ports.append(socket.getservbyname(port))
    except OSError:
        PSnotify.warn(f"{port} is not a valid service name - Skipping!")
    return ports


def get_ports_by_number(port: str) -> list[int]:
    """
    Docs
    """
    ports = []

    if port.isnumeric():
        ports.append(int(port))
    return ports


def get_ports_from_rule(rule_name: str) -> list[int]:
    """
    Docs
    """

    for rule in PSconstants.PORT_RULES:
        if rule['rule'] == rule_name:
            return rule['ports']
    PSnotify.warn(f"{rule_name} is not a valid ruleset - Skipping!")
    return []


def get_ports_from_rule_sets(port: str) -> list[int]:
    """
    Docs
    """
    ports = []

    match_results = re.search(r"ruleset:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        rule_sets = match_results.group(1)
        for rule in rule_sets.split(','):
            ports += get_ports_from_rule(rule)
    return ports


def get_ports_from_range(port: str) -> list[int]:
    """
    Get ports from a range
    """

    # Format A-B e.g. 1-1024
    result = re.search(r"(\d+)-(\d+)", port)
    if result is not None:
        return list(range(int(result.group(1)), int(result.group(2))))

    # Format A:B e.g.
    result = re.search(r"(\d+):(\d+)", port)
    if result is not None:
        return list(range(int(result.group(1)), int(result.group(2))))

    return []


def get_port_list_from_file(port: str) -> list[str]:
    """
    Docs
    """
    ports = []

    match_results = re.search(r"file:(.*)", port, re.IGNORECASE)
    if match_results is not None:
        fname = match_results.group(1)

        if not os.path.exists(fname):
            PSnotify.warn(f"{filename} does not exist - aborting")
        else:
            with open(fname, 'r', encoding='UTF-8') as f:
                lines = f.readlines()
                for line in lines:
                    for item in line.strip().split(','):
                        ports.append(item)
    return ports


def real_get_port_list(supplied_port_list: str) -> list[int]:
    """
    Docs
    """
    # This is order is important as once a port parameter is processed the loop is broken out of.
    functions_to_call = [get_ports_from_range, get_ports_from_rule_sets, get_ports_by_number, get_ports_by_name]
    generate_post_ports = []

    for port in supplied_port_list.split(','):
        for func in functions_to_call:
            port_list = func(port)
            if port_list:
                generate_post_ports += port_list
                break

    # Now we need to remove any duplicates and sort
    generate_post_ports = sorted(list(set(generate_post_ports)))

    return generate_post_ports


def get_port_list(supplied_port_list: str) -> list[int]:
    """
    Docs
    """
    # If there is a filename we need to pull the lists out of the file first!
    generated_port_list = []

    for port in supplied_port_list.split(','):
        port_list = get_port_list_from_file(port)
        if port_list:
            generated_port_list += port_list
        else:
            generated_port_list.append(port)

    return real_get_port_list(','.join(generated_port_list))

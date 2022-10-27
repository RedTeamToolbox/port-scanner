"""
Docs
"""

import re
import socket

import colored
from colored import stylize

import modules.globals as PSglobals

def list_all_port_rules():
    """
    Docs
    """

    print(stylize("Available rule sets:", colored.fg("cyan")))
    count = 0
    for rule in PSglobals.port_rules:
        count += 1
        print(f"  Rule {count}: '{rule['rule']}': {rule['ports']}")


def get_ports_from_rule(rule_name):
    """
    Docs
    """

    for rule in PSglobals.port_rules:
        if rule['rule'] == rule_name:
            return rule['ports']
    return None


def get_ports_from_rule_sets(rule_sets):
    """
    Docs
    """
    ports = []

    for rule in rule_sets.split(','):
        rule_ports = get_ports_from_rule(rule)
        if rule_ports is not None:
            ports += rule_ports
        else:
            print(stylize(f"{rule} is not a valid ruleset - Skipping!", colored.fg("yellow")))
    return ports


def get_port_list(port_list) -> list[int]:
    """
    Docs
    """
    ports = []

    for port in port_list.split(','):
        # Format A-B
        result = re.search(r"(\d+)-(\d+)", port)
        if result is not None:
            ports += (list(range(int(result.group(1)), int(result.group(2)))))
            continue

        # Format A:B
        result = re.search(r"(\d+):(\d+)", port)
        if result is not None:
            ports += (list(range(int(result.group(1)), int(result.group(2)))))
            continue

        match_results = re.search(r"ruleset:(.*)", port, re.IGNORECASE)
        if match_results is not None:
            ports += get_ports_from_rule_sets(match_results.group(1))
            continue

        # Just a normal number
        if port.isnumeric():
            ports.append(int(port))
            continue

        # Left with a string like sshd
        try:
            ports.append(socket.getservbyname(port))
        except OSError:
            print(stylize(f"{port} is not a valid service name - Skipping!", colored.fg("yellow")))
            continue

    # Now we need to remove any duplicates and sort
    ports = sorted(list(set(ports)))

    return ports

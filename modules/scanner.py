"""
Docs
"""

import argparse
import ipaddress
import re
import socket

from time import sleep
from typing import Any

import colored
from colored import stylize

import modules.globals as PSglobals
import modules.utils as PSutils

def scan_target_port(target, port, spinner, args: argparse.Namespace) -> dict[str, Any]:
    """
    docs
    """
    status = False
    error_msg = None
    banner = None

    if args.delay is True:
        sleep_time = PSutils.secure_random(1, args.delay_time)
        if args.verbose is True:
            spinner.write(stylize(f"Host: sleeping for {sleep_time} seconds", colored.fg("cyan")))
        sleep(sleep_time)

    if args.verbose is True:
        spinner.write(stylize(f"Host: {target} Testing Port: {port}", colored.fg("cyan")))

    ip = ipaddress.ip_address(target)
    if isinstance(ip, ipaddress.IPv6Address) is True:
        af_type = socket.AF_INET6
    else:
        af_type = socket.AF_INET

    with socket.socket(af_type, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((target, port))
            sock.settimeout(3)
            status = True
            try:
                banner = sock.recv(2048).decode('utf-8').strip()
            except socket.error as err:
                banner = 'Unavailable'
                error_msg = err
            sock.shutdown(0)
            sock.close()
        except socket.timeout:
            error_msg = "Connection timed out"
            status = False
        except socket.error as err:
            error_msg = str(err)
            result = re.search(r"(\[Errno \d+\] )?(.*)", error_msg)
            if result is not None:
                error_msg = result.group(2)
            status = False

    if args.verbose is True:
        spinner.write(stylize(f"Host: {target}, Port: {port}, Open?: {status}", colored.fg("cyan")))

    # Cache the service name in case we are hitting multiple IPs
    if port not in PSglobals.service_name_mapping:
        try:
            service = socket.getservbyport(port, 'tcp')
        except OSError:
            service = 'Unknown'
        PSglobals.service_name_mapping[port] = service

    return {
            'target': PSglobals.host_ip_mapping[target],
            'ip': ip,
            'ipnum': PSglobals.ip_ipnum_mapping[target],
            'port': port,
            'status': status,
            'service': PSglobals.service_name_mapping[port],
            'banner': banner,
            'error': error_msg
           }

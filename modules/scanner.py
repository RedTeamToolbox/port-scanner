"""
Docs
"""

import ipaddress
import re
import socket

from typing import Any

import modules.globals as PSglobals


def scan_target_port(target: str, port: int) -> dict[str, Any]:
    """
    docs
    """
    status = False
    status_string = 'Closed'
    error_msg = None
    banner = None

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
            status_string = 'Open'
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
            status_string = 'Closed'
            status = False
        except socket.error as err:
            error_msg = str(err)
            result = re.search(r"(\[Errno \d+\] )?(.*)", error_msg)
            if result is not None:
                error_msg = result.group(2)
            status_string = 'Closed'
            status = False

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
            'status_string': status_string,
            'service': PSglobals.service_name_mapping[port],
            'banner': banner,
            'error': error_msg
           }

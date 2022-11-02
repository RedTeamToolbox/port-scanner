# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import colorama

colorama.init()
RED: str = colorama.Fore.RED
YELLOW: str = colorama.Fore.YELLOW
GREEN: str = colorama.Fore.GREEN
GRAY: str = colorama.Fore.LIGHTBLACK_EX
RESET: str = colorama.Style.RESET_ALL

SUCCESS: str = colorama.Fore.GREEN
WARN: str = colorama.Fore.YELLOW
ERROR: str = colorama.Fore.RED
INFO: str = colorama.Fore.CYAN

PORT_RULES: list[dict] = [
    # all available ports
    {"rule": "all-ports", "ports": range(1, 65535)},
    # mssql server, mssql browser, ingres, mysql, postgresql
    {"rule": "databases", "ports": [1433, 1434, 1524, 3306, 5432]},
    # smtp, pop3, imap, submission
    {"rule": "email", "ports": [25, 110, 143, 587, 2525]},
    # ftp-data, ftp, tftp
    {"rule": "file-transfer", "ports": [20, 21, 69]},
    # name service, datagram service,  session service
    {"rule": "netbios", "ports": [137, 138, 139]},
    # ssh, telnet, remote desktop, VNC
    {"rule": "remote-access", "ports": [22, 23, 3389, 5900]},
    # samba
    {"rule": "samba", "ports": [445]},
    # http, https, http-alt, pcsync-https, pcsync-http
    {"rule": "web-servers", "ports": [80, 443, 8080, 8443, 8444]},
]

CLI_EPILOG: str = "For more detailed documentation please refer to: https://github.com/SecOpsToolbox/port-scanner"
CLI_DESC: str = "Check for open port(s) on target host(s)"
CLI_HELP: dict = {
    "help": "show this help message and exit",
    "quiet": "Do not show the results on the screen",
    "verbose": "Verbose output - show scan results as they come in",
    "ipv4-only": "Scan IPv4 addresses only",
    "ipv6-only": "Scan IPv6 addresses only",
    "all-results": "Show or save all results (default is to list open ports only)",
    "shuffle": "Randomise the scanning order",
    "list-rules": "List the available rules",
    "targets": "A comma separated list of targets to scan",
    "batch-size": "The size of the batch to use when splitting larger scan sets (0 = no batching)",
    "batch-delay": "The amount of time to wait between batches",
    "delay-time": "Random delay to use if --delay is given",
    "include-ports": "The ports you want to scan",
    "exclude-ports": "The ports you want to exclude from a scan",
    "threads": "The number of threads to use",
    "filename": "The filename to save the results to",
}

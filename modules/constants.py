"""
Constants live here
"""

import colorama

RED = colorama.Fore.RED
YELLOW = colorama.Fore.YELLOW
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Style.RESET_ALL

SUCCESS = colorama.Fore.GREEN
WARN = colorama.Fore.YELLOW
ERROR = colorama.Fore.RED
INFO = colorama.Fore.LIGHTBLACK_EX

epilog = "For more detailed documentation please refer to: https://github.com/SecOpsToolbox/port-scanner"

port_rules = [
    # mssql server, mssql browser, ingres, mysql, postgresql
    {'rule': 'databases', 'ports': [1433, 1434, 1524, 3306, 5432]},
    # smtp, pop3, imap, submission
    {'rule': 'email', 'ports': [25, 110, 143, 587, 2525]},
    # ftp-data, ftp, tftp
    {'rule': 'file-transfer', 'ports': [20, 21, 69]},
    # name service, datagram service,  session service
    {'rule': 'netbios', 'ports': [137, 138, 139]},
    # ssh, telnet, remote desktop, VNC
    {'rule': 'remote-access', 'ports': [22, 23, 3389, 5900]},
    # samba
    {'rule': 'samba', 'ports': [445]},
    # http, https, http-alt, pcsync-https, pcsync-http
    {'rule': 'web-servers', 'ports': [80, 443, 8080, 8443, 8444]},
]

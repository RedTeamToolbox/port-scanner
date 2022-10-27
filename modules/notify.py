"""
User based notifications
"""

import modules.constants as PSconstants


def success(message: str) -> None:
    """
    Docs
    """
    print(f"{PSconstants.SUCCESS}{message}{PSconstants.RESET}")


def warn(message: str) -> None:
    """
    Docs
    """
    print(f"{PSconstants.WARN}{message}{PSconstants.RESET}")


def error(message: str) -> None:
    """
    Docs
    """
    print(f"{PSconstants.ERROR}{message}{PSconstants.RESET}")


def info(message: str) -> None:
    """
    Docs
    """
    print(f"{PSconstants.INFO}{message}{PSconstants.RESET}")

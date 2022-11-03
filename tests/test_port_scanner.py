# -*- coding: utf-8 -*-

"""This is the summary line.

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""
from typing import Any

from modules.constants import ERROR, INFO, SUCCESS, WARN, RESET
from modules.globals import host_ip_mapping, ip_ipnum_mapping, service_name_mapping
from modules.notify import error, error_msg, info, info_msg, success, success_msg, warn, warn_msg
from modules.ordering import multikeysort, shuffled
from modules.random import secure_random


def output_errors(errors: list, header="Errors occurred:") -> str:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        errors (list) -- _description_

    Keyword Arguments:
        header (str) -- _description_ (default: "Errors occurred:")

    Returns:
        str -- _description_
    """
    error_string: str = header
    for err in errors:
        error_string += f"{err}\n"
    return error_string


def test_notify(capsys) -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.

    Arguments:
        capfd (_type_) -- _description_
    """
    test_cases: dict = {
        success: SUCCESS,
        warn: WARN,
        error: ERROR,
        info: INFO,
    }
    errors: list = []
    count: int = 0
    clean_string: str = "hello world"
    result_string: str = ''

    for test_function, color_code in test_cases.items():
        count += 1
        test_string: str = f"{color_code}{clean_string}{RESET}"
        test_function(clean_string)
        captured = capsys.readouterr()
        result_string = captured.out

        if test_string != result_string.strip():
            errors.append(f"Test {count} failed: {test_string} vs {result_string}")

    assert not errors, output_errors(errors)  # nosec: B101


def test_notify_messages() -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.
    """
    test_cases: dict = {
        success_msg: SUCCESS,
        warn_msg: WARN,
        error_msg: ERROR,
        info_msg: INFO,
    }
    errors: list = []
    count: int = 0
    clean_string: str = "hello world"
    result_string: str = ''

    for test_function, color_code in test_cases.items():
        count += 1
        test_string: str = f"{color_code}{clean_string}{RESET}"
        result_string = test_function(clean_string)

        if test_string != result_string:
            errors.append(f"Test {count} failed: {test_string} vs {result_string}")

    assert not errors, output_errors(errors)  # nosec: B101


def test_globals() -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.
    """
    tests: list = [host_ip_mapping, ip_ipnum_mapping, service_name_mapping]
    errors: list = []
    count: int = 0

    for test in tests:
        count += 1
        if test:
            errors.append(f"Test {count} get_ports_by_name'ssh' failed: (not empty)")

    assert not errors, output_errors(errors)  # nosec: B101


def test_utils() -> None:
    """Define a summary.

    This is the extended summary from the template and needs to be replaced.
    """
    errors: list = []
    count: int = 0
    test_list: list[int] = [1, 2, 3, 4, 5]
    test_list_2: list = [1, 2, 3, 4, 5, ["a", "b", "c"]]

    multisort_test_list: list[dict[str, str]] = [{"name": "wolf"}, {"name": "software"}]
    multisort_sorted_list: list[dict[str, str]] = [{"name": "software"}, {"name": "wolf"}]

    rint: int = secure_random(1, 10)
    count += 1
    if rint not in range(1, 11):
        errors.append(f"Test {count} security_random failed: {rint}")

    slist: list[Any] = shuffled(test_list, 0)
    count += 1
    if slist != test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    slist = shuffled(test_list)
    count += 1
    if slist == test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    slist = shuffled(test_list_2)
    count += 1
    if slist == test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    count += 1
    sorted_list: list[dict] = multikeysort(multisort_test_list, ['name'])
    if sorted_list != multisort_sorted_list:
        errors.append(f"Test {count} multi sort failed: {multisort_test_list} vs {multisort_sorted_list}")

    assert not errors, output_errors(errors)  # nosec: B101

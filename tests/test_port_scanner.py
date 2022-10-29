# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import modules.constants as PSconstants
import modules.globals as PSglobal
import modules.notify as PSnotify
import modules.ports as PSports
import modules.utils as PSutils


def output_errors(errors, header = "Errors occurred:"):
    """_summary_

    _extended_summary_

    Arguments:
        errors (_type_) -- _description_

    Keyword Arguments:
        header (str) -- _description_ (default: "Errors occurred:")
    """

    print(header)
    for error in errors:
        print(error)


def test_notify(capfd) -> None:
    """_summary_

    _extended_summary_

    Arguments:
        capfd (_type_) -- _description_
    """
    tests = [
              {"function": PSnotify.success, "color": PSconstants.SUCCESS, "strip": True, "return_value": False},
              {"function": PSnotify.warn, "color": PSconstants.WARN, "strip": True, "return_value": False},
              {"function": PSnotify.error, "color": PSconstants.ERROR, "strip": True, "return_value": False},
              {"function": PSnotify.info, "color": PSconstants.INFO, "strip": True, "return_value": False},
              {"function": PSnotify.success_msg, "color": PSconstants.SUCCESS, "strip": False, "return_value": True},
              {"function": PSnotify.warn_msg, "color": PSconstants.WARN, "strip": False, "return_value": True},
              {"function": PSnotify.error_msg, "color": PSconstants.ERROR, "strip": False, "return_value": True},
              {"function": PSnotify.info_msg, "color": PSconstants.INFO, "strip": False, "return_value": True},
    ]
    errors = []
    count = 0
    clean_string = "hello world"

    for test in tests:
        count += 1
        test_string = f"{test['color']}{clean_string}{PSconstants.RESET}"

        if test['return_value'] is True:
            result_string = test['function'](clean_string)  # pylint: disable=assignment-from-no-return
        else:
            test['function'](clean_string)
            result_string, _err = capfd.readouterr()

        if test['strip'] is True:
            result_string = result_string.strip()
        if test_string != result_string:
            errors.append(f"Test {count} failed: {test_string} vs {result_string}")

    assert not errors, output_errors(errors)  # nosec: B101


def test_globals() -> None:
    """_summary_

    _extended_summary_
    """
    tests = [PSglobal.host_ip_mapping, PSglobal.ip_ipnum_mapping, PSglobal.service_name_mapping]
    errors = []
    count = 0

    for test in tests:
        count += 1
        if test:
            errors.append(f"Test {count} get_ports_by_name'ssh' failed: (not empty)")

    assert not errors, output_errors(errors)  # nosec: B101


def test_ports() -> None:
    """_summary_

    _extended_summary_
    """
    errors = []
    count = 0

    port = PSports.get_ports_by_number("22")
    count += 1
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    port = PSports.get_ports_by_name("ssh")
    count += 1
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    assert not errors, output_errors(errors)  # nosec: B101


def test_utils() -> None:
    """_summary_

    _extended_summary_
    """
    errors = []
    count = 0
    test_list = [1, 2, 3, 4, 5]
    test_list_2 = [1, 2, 3, 4, 5, ["a", "b", "c"]]

    multisort_test_list = [{"name": "wolf"}, {"name": "software"}]
    multisort_sorted_list = [{"name": "software"}, {"name": "wolf"}]

    rint = PSutils.secure_random(1, 10)
    count += 1
    if rint not in range(1, 11):
        errors.append(f"Test {count} security_random failed: {rint}")

    slist = PSutils.shuffled(test_list, 0)
    count += 1
    if slist != test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    slist = PSutils.shuffled(test_list)
    count += 1
    if slist == test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    slist = PSutils.shuffled(test_list_2)
    count += 1
    if slist == test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    count += 1
    sorted_list = PSutils.multikeysort(multisort_test_list, ['name'])
    if sorted_list != multisort_sorted_list:
        errors.append(f"Test {count} multi sort failed: {multisort_test_list} vs {multisort_sorted_list}")

    assert not errors, output_errors(errors)  # nosec: B101

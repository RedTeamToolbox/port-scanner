"""
Docs
"""

import modules.constants as PSconstants
import modules.globals as PSglobal
import modules.notify as PSnotify
import modules.ports as PSports
import modules.utils as PSutils

ERRORS_OCCURRED = "errors occurred:\n"


def test_notify(capfd) -> None:
    """
    test notify
    """
    tests = [
              {'function': PSnotify.success, 'color': PSconstants.SUCCESS, 'strip': True, 'return_value': False},
              {'function': PSnotify.warn, 'color': PSconstants.WARN, 'strip': True, 'return_value': False},
              {'function': PSnotify.error, 'color': PSconstants.ERROR, 'strip': True, 'return_value': False},
              {'function': PSnotify.info, 'color': PSconstants.INFO, 'strip': True, 'return_value': False},
              {'function': PSnotify.success_msg, 'color': PSconstants.SUCCESS, 'strip': False, 'return_value': True},
              {'function': PSnotify.warn_msg, 'color': PSconstants.WARN, 'strip': False, 'return_value': True},
              {'function': PSnotify.error_msg, 'color': PSconstants.ERROR, 'strip': False, 'return_value': True},
              {'function': PSnotify.info_msg, 'color': PSconstants.INFO, 'strip': False, 'return_value': True},
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

    if errors:
        errors_list = "\n".join(errors)
        assert f"{ERRORS_OCCURRED}\n{errors_list}"  # nosec: B101


def test_globals() -> None:
    """
    Docs
    """
    tests = [PSglobal.host_ip_mapping, PSglobal.ip_ipnum_mapping, PSglobal.service_name_mapping]
    errors = []
    count = 0

    for test in tests:
        count += 1
        if test:
            errors.append(f"Test {count} get_ports_by_name'ssh' failed: (not empty)")

    if errors:
        errors_list = "\n".join(errors)
        assert f"{ERRORS_OCCURRED}\n{errors_list}"  # nosec: B101


def test_ports() -> None:
    """
    Docs
    """
    errors = []
    count = 0

    port = PSports.get_ports_by_number('22')
    count += 1
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    port = PSports.get_ports_by_name('ssh')
    count += 1
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    if errors:
        errors_list = "\n".join(errors)
        assert f"{ERRORS_OCCURRED}\n{errors_list}"  # nosec: B101


def test_utils() -> None:
    """
    Docs
    """
    errors = []
    count = 0
    test_list = [1, 2, 3, 4, 5]
    test_list_2 = [1, 2, 3, 4, 5, ['a', 'b', 'c']]

    multisort_test_list = [{'name': 'wolf'}, {'name': 'software'}]
    multisort_sorted_list = [{'name': 'software'}, {'name': 'wolf'}]

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

    if errors:
        errors_list = "\n".join(errors)
        assert f"{ERRORS_OCCURRED}\n{errors_list}"  # nosec: B101

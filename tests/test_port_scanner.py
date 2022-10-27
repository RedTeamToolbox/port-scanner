"""
Docs
"""

import modules.constants as PSconstants
import modules.notify as PSnotify
import modules.ports as PSports
import modules.utils as PSutils


def test_notify(capfd) -> None:
    """
    test notify
    """
    errors = []
    count = 0

    test_string = f"{PSconstants.SUCCESS}test{PSconstants.RESET}"
    PSnotify.success("test")
    out, err = capfd.readouterr()
    if test_string != out.strip():
        errors.append(f"Test success failed '{test_string}' vs '{out}'")

    test_string = f"{PSconstants.WARN}test{PSconstants.RESET}"
    PSnotify.warn("test")
    out, err = capfd.readouterr()
    if test_string != out.strip():
        errors.append(f"Test warn failed '{test_string}' vs '{out}'")

    test_string = f"{PSconstants.ERROR}test{PSconstants.RESET}"
    PSnotify.error("test")
    out, err = capfd.readouterr()
    if test_string != out.strip():
        errors.append(f"Test error failed '{test_string}' vs '{out}'")

    test_string = f"{PSconstants.INFO}test{PSconstants.RESET}"
    PSnotify.info("test")
    out, err = capfd.readouterr()
    if test_string != out.strip():
        errors.append(f"Test info failed '{test_string}' vs '{out}'")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101


def test_ports() -> None:
    """
    Docs
    """
    errors = []
    count = 0

    port = PSports.get_ports_by_number('22')
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    port = PSports.get_ports_by_name('ssh')
    if port != [22]:
        errors.append(f"Test {count} get_ports_by_name'ssh' failed: {port}")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101


def test_utils() -> None:
    """
    Docs
    """
    errors = []
    count = 0
    test_list = [1, 2, 3, 4, 5]

    rint = PSutils.secure_random(1, 10)
    if rint not in range(1, 11):
        errors.append(f"Test {count} security_random failed: {rint}")

    slist = PSutils.shuffled(test_list)
    if slist == test_list:
        errors.append(f"Test {count} shuffled failed failed: {slist}")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101

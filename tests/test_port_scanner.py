"""
Docs
"""
import modules.ports as PSports
import modules.utils as PSutils


def test_ports() -> None:
    """
    Docs
    """
    errors = []
    count = 0

    if PSports.get_ports_by_number('22') != 22:
        errors.append(f"Test {count} get_ports_by_name'ssh'")

    if PSports.get_ports_by_name('ssh') != 22:
        errors.append(f"Test {count} get_ports_by_name'ssh'")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101


def test_utils() -> None:
    """
    Docs
    """
    errors = []
    count = 0
    test_list = [1, 2, 3, 4, 5]

    v = PSutils.secure_random(1, 10)
    if v not in range(1, 10):
        errors.append(f"Test {count} security_random failed")

    v = PSutils.shuffled(test_list)
    if v == test_list:
        errors.append(f"Test {count} shuffled failed failed")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101

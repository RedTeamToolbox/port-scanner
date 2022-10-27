"""
Docs
"""

import modules.utils as PSutils


def test_secure_random() -> None:
    """
    Docs
    """
    errors = []
    count = 0

    v = PSutils.secure_random(1, 10)
    if v not in range(1, 10):
        errors.append(f"Test {count} security_random failed")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101


def test_shuffled() -> None:
    """
    Docs
    """
    errors = []
    count = 0

    test_list = [1, 2, 3, 4, 5]

    v = PSutils.shuffled(test_list)
    if v == test_list:
        errors.append(f"Test {count} shuffled failed failed")

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))  # nosec: B101

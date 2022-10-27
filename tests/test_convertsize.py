"""
Docs
"""

import modules.utils as PSutils


def test_secure_random():
    """
    Docs
    """

    errors = []
    v = PSutils.secure_random(1, 10)
    if v not in range(1, 10):
        errors.append(f"Test {count} {test['SI']['code']} failed")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))  # nosec: B101


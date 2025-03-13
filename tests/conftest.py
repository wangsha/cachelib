import os
import warnings
from pathlib import Path

import pytest


def under_uwsgi():
    try:
        import uwsgi  # noqa: F401
    except ImportError:
        return False
    else:
        return True


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    if under_uwsgi():
        try:
            script_path = Path(os.environ["TMPDIR"], "return_pytest_exit_code.py")
        except KeyError:
            warnings.warn(
                "Pytest could not find tox 'TMPDIR' in the environment,"
                " make sure the variable is set in the project tox.ini"
                " file if you are running under tox.",
                stacklevel=2,
            )
        else:
            with open(script_path, mode="w") as f:
                f.write(f"import sys; sys.exit({exitstatus})")


class TestData:
    """This class centralizes all data samples used in tests"""

    sample_numbers = [0, 10, 1024000, 9, 5000000000000, 99, 738, 2000000]
    sample_pairs = {
        "128": False,
        "beef": True,
        "crevettes": {},
        "1024": "spam",
        "bacon": "eggs",
        "sausage": 2048,
        "3072": [],
        "brandy": [{}, "fried eggs"],
        "lobster": ["baked beans", [512]],
        "4096": {"sauce": [], 256: "truffle"},
    }

import os
import sys
import copy
import pytest

# ensure src directory is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import app  # noqa: E402

@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    return TestClient(app.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Deep-copy the original activities dict from the module and restore it before
    each test.  This keeps tests isolated even though the application uses a
    mutable global.
    """
    original = copy.deepcopy(app.activities)
    yield
    app.activities.clear()
    app.activities.update(original)

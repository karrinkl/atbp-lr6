import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")


@pytest.fixture(scope="session")
def browser(launch_browser):
    try:
        browser_instance = launch_browser()
    except Exception as exc:
        pytest.skip(f"UI tests are skipped: Playwright browser is unavailable ({exc})")
    yield browser_instance
    browser_instance.close()

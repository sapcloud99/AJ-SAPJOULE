"""Test-specific conftest: ensure app/ is on sys.path for all tests in this folder."""
import pytest


@pytest.fixture(autouse=True)
def _ensure_app_on_path(add_agent_to_path):
    """Auto-use the add_agent_to_path fixture from the root conftest."""
    yield

"""
Pytest configuration file for shared fixtures and settings
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path so we can import the app
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Configure pytest
pytest_plugins = []


@pytest.fixture(scope="session")
def project_root_path():
    """Return the project root path"""
    return Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Any global test setup can go here
    yield
    # Any global test cleanup can go here
    pass
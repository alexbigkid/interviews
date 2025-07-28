"""Tests for hello_global_logic module."""

from io import StringIO
import sys
from gl_011.hello_global_logic import hello


def test_hello_output():
    """Test that hello function prints correct message."""
    captured_output = StringIO()
    sys.stdout = captured_output

    hello()

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert output == "Hello Global Logic!"


def test_hello_function_exists():
    """Test that hello function exists and is callable."""
    assert callable(hello)
    assert hello.__doc__ == "Hello Global Logic function."

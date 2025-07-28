"""Tests for meta_data module."""

from unittest.mock import MagicMock, patch

import pytest
from gl_011.meta_data import (
    process_metadata_item,
    handle_processing_error,
    log_progress,
    on_completed,
    on_error,
    main,
    metadata_list,
)


def test_process_metadata_item_success():
    """Test process_metadata_item with successful processing."""
    metadata = {"id": 1, "value": "Item 1"}

    with (
        patch("gl_011.meta_data.random.random", return_value=0.5),
        patch("gl_011.meta_data.time.sleep"),
    ):
        result = process_metadata_item(metadata)
        assert result == "Processed Item 1"


def test_process_metadata_item_failure():
    """Test process_metadata_item with failure (random < 0.2)."""
    metadata = {"id": 1, "value": "Item 1"}

    with (
        patch("gl_011.meta_data.random.random", return_value=0.1),
        pytest.raises(ValueError, match="Failed to process"),
    ):
        process_metadata_item(metadata)


def test_handle_processing_error(capsys):
    """Test handle_processing_error function."""
    error = ValueError("Test error")
    metadata = {"id": 1, "value": "Item 1"}

    result = handle_processing_error(error, metadata)

    # Check that error was printed
    captured = capsys.readouterr()
    assert "[Error Handler]" in captured.out
    assert "Test error" in captured.out

    # Check that empty observable is returned
    assert result is not None


def test_log_progress(capsys):
    """Test log_progress function."""
    result = "Test progress message"

    log_progress(result)

    captured = capsys.readouterr()
    assert "🚀 [Progress] Test progress message" in captured.out


def test_on_completed(capsys):
    """Test on_completed callback."""
    on_completed()

    captured = capsys.readouterr()
    assert "✅ All metadata processed." in captured.out


def test_on_error(capsys):
    """Test on_error callback."""
    error = Exception("Test error")

    on_error(error)

    captured = capsys.readouterr()
    assert "❌ Stream failed: Test error" in captured.out


def test_metadata_list():
    """Test that metadata_list is properly initialized."""
    assert len(metadata_list) == 10
    assert metadata_list[0] == {"id": 0, "value": "Item 0"}
    assert metadata_list[9] == {"id": 9, "value": "Item 9"}


def test_main_function(capsys):
    """Test main function execution."""
    # Mock the reactive pipeline to avoid actual execution
    with patch("gl_011.meta_data.rx.from_iterable") as mock_from_iterable:
        mock_observable = MagicMock()
        mock_from_iterable.return_value = mock_observable
        mock_observable.pipe.return_value = mock_observable
        mock_observable.subscribe.return_value = None

        # Mock threading.Event to simulate immediate completion
        with patch("gl_011.meta_data.threading.Event") as mock_event_class:
            mock_event = MagicMock()
            mock_event.wait.return_value = True  # Simulate successful completion
            mock_event_class.return_value = mock_event

            main()

            # Verify that the reactive pipeline was set up
            mock_from_iterable.assert_called_once_with(metadata_list)
            mock_observable.pipe.assert_called_once()
            mock_observable.subscribe.assert_called_once()

            # Verify that done_event.wait was called
            mock_event.wait.assert_called_once_with(timeout=30)

            # Check that completion message was printed
            captured = capsys.readouterr()
            assert "🎉 Processing completed" in captured.out


def test_main_function_timeout(capsys):
    """Test main function with timeout scenario."""
    with patch("gl_011.meta_data.rx.from_iterable") as mock_from_iterable:
        mock_observable = MagicMock()
        mock_from_iterable.return_value = mock_observable
        mock_observable.pipe.return_value = mock_observable
        mock_observable.subscribe.return_value = None

        # Mock threading.Event to simulate timeout
        with patch("gl_011.meta_data.threading.Event") as mock_event_class:
            mock_event = MagicMock()
            mock_event.wait.return_value = False  # Simulate timeout
            mock_event_class.return_value = mock_event

            main()

            # Verify timeout message was printed
            captured = capsys.readouterr()
            assert "❌ Timed out waiting for all processing to complete." in captured.out


def test_metadata_item_structure():
    """Test that metadata items have correct structure."""
    for item in metadata_list:
        assert "id" in item
        assert "value" in item
        assert isinstance(item["id"], int)
        assert isinstance(item["value"], str)
        assert item["value"].startswith("Item ")


def test_threading_components():
    """Test that threading components are imported and available."""
    import threading

    # Test that we can create threading primitives
    lock = threading.Lock()
    event = threading.Event()

    assert lock is not None
    assert event is not None
    assert hasattr(event, "wait")
    assert hasattr(event, "set")

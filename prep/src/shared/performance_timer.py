"""Performance timer."""

# Standard library imports
import timeit


class PerformanceTimer:
    """Calculates time spent. Should be used as context manager."""

    def __init__(self, timer_name, logger):
        """Init for performance timer."""
        self._timer_name = timer_name
        self._logger = logger

    def __enter__(self):
        """Enter for performance timer."""
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit for performance timer."""
        _ = exc_type, exc_value, traceback  # Unused parameters
        time_took = (timeit.default_timer() - self.start) * 1000.0
        self._logger.info(f"Executing {self._timer_name} took {str(time_took)} ms")


if __name__ == "__main__":
    raise RuntimeError("This module is not meant to be run directly. Only for imports.")

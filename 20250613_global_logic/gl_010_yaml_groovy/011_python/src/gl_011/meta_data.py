"""Metadata processing module using ReactiveX for concurrent pipeline processing."""

import random
import threading
import time

import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler import ThreadPoolScheduler

# Modern Python 3.13+ types
metadata_list: list[dict[str, str | int]] = [{"id": i, "value": f"Item {i}"} for i in range(10)]

# Use a thread pool for concurrency
scheduler = ThreadPoolScheduler(max_workers=5)


def process_metadata_item(metadata: dict[str, str | int]) -> str | None:
    """Process a metadata item with simulated failure rate."""
    if random.random() < 0.2:
        raise ValueError(f"Failed to process: {metadata}")
    time.sleep(random.uniform(0.1, 0.3))
    return f"Processed {metadata['value']}"


def handle_processing_error(e: Exception, metadata: dict) -> rx.Observable:
    """Handle processing errors by logging and returning empty observable."""
    print(f"[Error Handler] {e} for {metadata}")
    return rx.empty()


def log_progress(result: str) -> None:
    """Log processing progress."""
    print(f"🚀 [Progress] {result}")


def on_completed() -> None:
    """Callback for when all processing is completed."""
    print("✅ All metadata processed.")


def on_error(error: Exception) -> None:
    """Callback for when an unhandled error occurs in the stream."""
    print(f"❌ Stream failed: {error}")


def main() -> None:
    """Main function to run the metadata processing pipeline."""
    completed = 0
    total = len(metadata_list)
    lock = threading.Lock()
    done_event = threading.Event()

    def log_progress_with_count(result: str) -> None:
        """Log processing progress with completion count."""
        nonlocal completed
        with lock:
            completed += 1
            print(f"🚀 [Progress] {result} ({completed}/{total})")

    def on_completed_with_event() -> None:
        """Callback for when all processing is completed."""
        print("✅ All metadata processed.")
        done_event.set()

    def on_error_with_event(error: Exception) -> None:
        """Callback for when an unhandled error occurs in the stream."""
        print(f"❌ Stream failed: {error}")
        done_event.set()

    # Reactive pipeline using Python 3.13 syntax
    rx.from_iterable(metadata_list).pipe(
        ops.flat_map(
            lambda metadata: rx.of(metadata).pipe(
                ops.subscribe_on(scheduler),
                ops.map(process_metadata_item),
                ops.retry(2),
                ops.catch(lambda e, _: handle_processing_error(e, metadata)),
                ops.filter(lambda result: result is not None),
                ops.do_action(log_progress_with_count),
            )
        )
    ).subscribe(on_completed=on_completed_with_event, on_error=on_error_with_event)

    # Wait for all processing to complete with timeout
    if not done_event.wait(timeout=30):
        print("❌ Timed out waiting for all processing to complete.")
    else:
        print(f"🎉 Processing completed: {completed}/{total} items processed successfully.")


if __name__ == "__main__":
    main()

"""Advanced batching and array processing problems for interview preparation."""

from typing import Any
from collections import deque


def batch_process(data: list[Any], batch_size: int) -> list[list[Any]]:
    """Split data into batches of specified size.

    Time: O(n), Space: O(n)

    Args:
        data: Input data to batch
        batch_size: Size of each batch

    Returns:
        List of batches, last batch may be smaller

    Examples:
        >>> batch_process([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> batch_process(["a", "b", "c", "d"], 3)
        [['a', 'b', 'c'], ['d']]
        >>> batch_process([], 2)
        []
    """
    if not data or batch_size <= 0:
        return []

    batches = []
    for i in range(0, len(data), batch_size):
        batches.append(data[i : i + batch_size])
    return batches


def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    """Find maximum in each sliding window of size k.

    Time: O(n), Space: O(k)

    Args:
        nums: Input array
        k: Window size

    Returns:
        Maximum in each window

    Examples:
        >>> sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [3, 3, 5, 5, 6, 7]
        >>> sliding_window_maximum([1], 1)
        [1]
        >>> sliding_window_maximum([1, -1], 1)
        [1, -1]
    """
    if not nums or k <= 0:
        return []

    dq = deque()  # Store indices
    result = []

    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices with smaller values (maintain decreasing order)
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()

        dq.append(i)

        # Add maximum to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def sliding_window_minimum(nums: list[int], k: int) -> list[int]:
    """Find minimum in each sliding window of size k.

    Time: O(n), Space: O(k)

    Args:
        nums: Input array
        k: Window size

    Returns:
        Minimum in each window

    Examples:
        >>> sliding_window_minimum([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [-1, -3, -3, -3, 3, 3]
        >>> sliding_window_minimum([1], 1)
        [1]
    """
    if not nums or k <= 0:
        return []

    dq = deque()  # Store indices
    result = []

    for i in range(len(nums)):
        # Remove indices outside current window
        while dq and dq[0] <= i - k:
            dq.popleft()

        # Remove indices with larger values (maintain increasing order)
        while dq and nums[dq[-1]] >= nums[i]:
            dq.pop()

        dq.append(i)

        # Add minimum to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def longest_subarray_sum_k(nums: list[int], k: int) -> int:
    """Find length of longest subarray with sum equal to k.

    Time: O(n), Space: O(n)

    Args:
        nums: Array of integers
        k: Target sum

    Returns:
        Length of longest subarray with sum k

    Examples:
        >>> longest_subarray_sum_k([1, -1, 5, -2, 3], 3)
        4
        >>> longest_subarray_sum_k([1, 2, 3], 3)
        1
        >>> longest_subarray_sum_k([1, 1, 1], 2)
        2
    """
    if not nums:
        return 0

    prefix_sum_map = {0: -1}  # prefix_sum -> earliest_index
    prefix_sum = 0
    max_length = 0

    for i, num in enumerate(nums):
        prefix_sum += num

        # Check if there's a previous prefix_sum such that current - previous = k
        if prefix_sum - k in prefix_sum_map:
            length = i - prefix_sum_map[prefix_sum - k]
            max_length = max(max_length, length)

        # Only store first occurrence to maximize length
        if prefix_sum not in prefix_sum_map:
            prefix_sum_map[prefix_sum] = i

    return max_length


def min_subarray_sum_target(target: int, nums: list[int]) -> int:
    """Find minimum length subarray with sum >= target.

    Time: O(n), Space: O(1)

    Args:
        target: Target sum
        nums: Array of positive integers

    Returns:
        Minimum length, 0 if impossible

    Examples:
        >>> min_subarray_sum_target(7, [2, 3, 1, 2, 4, 3])
        2
        >>> min_subarray_sum_target(4, [1, 4, 4])
        1
        >>> min_subarray_sum_target(11, [1, 1, 1, 1, 1, 1, 1, 1])
        0
    """
    if not nums or target <= 0:
        return 0

    left = 0
    min_length = float("inf")
    window_sum = 0

    for right in range(len(nums)):
        window_sum += nums[right]

        while window_sum >= target and left <= right:
            min_length = min(min_length, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return min_length if min_length != float("inf") else 0


def frequency_based_batching(items: list[str], batch_size: int) -> list[list[str]]:
    """Create batches prioritizing most frequent items first.

    Time: O(n log n), Space: O(n)

    Args:
        items: List of items to batch
        batch_size: Maximum items per batch

    Returns:
        Batches with frequent items prioritized

    Examples:
        >>> frequency_based_batching(["a", "b", "a", "c", "a", "b"], 2)
        [['a', 'a'], ['a', 'b'], ['b', 'c']]
    """
    if not items or batch_size <= 0:
        return []

    # Count frequencies
    from collections import Counter

    freq_count = Counter(items)

    # Sort by frequency (descending), then by item (for stability)
    sorted_items = sorted(items, key=lambda x: (-freq_count[x], x))

    # Create batches
    batches = []
    for i in range(0, len(sorted_items), batch_size):
        batches.append(sorted_items[i : i + batch_size])

    return batches


def balanced_batching(items: list[tuple[str, int]], max_weight: int) -> list[list[tuple[str, int]]]:
    """Create batches respecting weight constraints.

    Time: O(n), Space: O(n)

    Args:
        items: List of (item, weight) tuples
        max_weight: Maximum weight per batch

    Returns:
        Batches respecting weight limits

    Examples:
        >>> balanced_batching([("a", 3), ("b", 2), ("c", 4), ("d", 1)], 5)
        [[('a', 3), ('b', 2)], [('c', 4), ('d', 1)]]
    """
    if not items or max_weight <= 0:
        return []

    batches = []
    current_batch = []
    current_weight = 0

    for item, weight in items:
        if weight > max_weight:
            # Item too heavy for any batch, add it separately
            if current_batch:
                batches.append(current_batch)
                current_batch = []
                current_weight = 0
            batches.append([(item, weight)])  # Include the heavy item
            continue

        if current_weight + weight <= max_weight:
            current_batch.append((item, weight))
            current_weight += weight
        else:
            # Start new batch
            if current_batch:
                batches.append(current_batch)
            current_batch = [(item, weight)]
            current_weight = weight

    # Add last batch if not empty
    if current_batch:
        batches.append(current_batch)

    return batches


def time_window_batching(events: list[tuple[int, Any]], window_size: int) -> list[list[tuple[int, Any]]]:
    """Batch events within time windows.

    Time: O(n), Space: O(n)

    Args:
        events: List of (timestamp, data) tuples
        window_size: Size of time window

    Returns:
        Batches of events within time windows

    Examples:
        >>> time_window_batching([(1, "a"), (2, "b"), (5, "c"), (6, "d")], 3)
        [[(1, 'a'), (2, 'b')], [(5, 'c'), (6, 'd')]]
    """
    if not events or window_size <= 0:
        return []

    # Sort events by timestamp
    sorted_events = sorted(events, key=lambda x: x[0])

    batches = []
    current_batch = []
    window_start = None

    for timestamp, data in sorted_events:
        if window_start is None:
            window_start = timestamp
            current_batch = [(timestamp, data)]
        elif timestamp <= window_start + window_size:
            current_batch.append((timestamp, data))
        else:
            # Start new window
            if current_batch:
                batches.append(current_batch)
            window_start = timestamp
            current_batch = [(timestamp, data)]

    # Add last batch if not empty
    if current_batch:
        batches.append(current_batch)

    return batches


def circular_array_rotation(nums: list[int], k: int) -> list[int]:
    """Rotate array to the right by k steps.

    Time: O(n), Space: O(1)

    Args:
        nums: Array to rotate
        k: Number of steps to rotate right

    Returns:
        Rotated array

    Examples:
        >>> circular_array_rotation([1, 2, 3, 4, 5, 6, 7], 3)
        [5, 6, 7, 1, 2, 3, 4]
        >>> circular_array_rotation([-1, -100, 3, 99], 2)
        [3, 99, -1, -100]
    """
    if not nums or k == 0:
        return nums[:]

    n = len(nums)
    k = k % n  # Handle k > n

    # Three-step reversal approach
    def reverse(arr, start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1

    result = nums[:]
    reverse(result, 0, n - 1)  # Reverse entire array
    reverse(result, 0, k - 1)  # Reverse first k elements
    reverse(result, k, n - 1)  # Reverse remaining elements

    return result


def interleave_arrays(arr1: list[Any], arr2: list[Any]) -> list[Any]:
    """Interleave two arrays element by element.

    Time: O(n + m), Space: O(n + m)

    Args:
        arr1: First array
        arr2: Second array

    Returns:
        Interleaved array

    Examples:
        >>> interleave_arrays([1, 3, 5], [2, 4, 6])
        [1, 2, 3, 4, 5, 6]
        >>> interleave_arrays(["a", "c"], ["b", "d", "e"])
        ['a', 'b', 'c', 'd', 'e']
    """
    result = []
    i = j = 0

    # Interleave while both arrays have elements
    while i < len(arr1) and j < len(arr2):
        result.append(arr1[i])
        result.append(arr2[j])
        i += 1
        j += 1

    # Add remaining elements from longer array
    while i < len(arr1):
        result.append(arr1[i])
        i += 1

    while j < len(arr2):
        result.append(arr2[j])
        j += 1

    return result


def find_duplicates_linear(nums: list[int]) -> list[int]:
    """Find all duplicates in array where 1 ≤ a[i] ≤ n.

    Time: O(n), Space: O(1)

    Args:
        nums: Array of integers

    Returns:
        List of duplicate numbers

    Examples:
        >>> find_duplicates_linear([4, 3, 2, 7, 8, 2, 3, 1])
        [2, 3]
        >>> find_duplicates_linear([1, 1, 2])
        [1]
        >>> find_duplicates_linear([1])
        []
    """
    if not nums:
        return []

    duplicates = []

    # Use array indices as hash map
    for i in range(len(nums)):
        num = abs(nums[i])
        idx = num - 1  # Convert to 0-based index
        if nums[idx] < 0:
            # Already marked, so this is a duplicate
            duplicates.append(num)
        else:
            # Mark as seen by making negative
            nums[idx] = -nums[idx]

    # Restore original array
    for i in range(len(nums)):
        nums[i] = abs(nums[i])

    return duplicates


def majority_element_n3(nums: list[int]) -> list[int]:
    """Find all elements appearing more than n/3 times.

    Time: O(n), Space: O(1)

    Args:
        nums: Input array

    Returns:
        Elements appearing more than n/3 times

    Examples:
        >>> majority_element_n3([3, 2, 3])
        [3]
        >>> majority_element_n3([1])
        [1]
        >>> majority_element_n3([1, 2])
        [1, 2]
    """
    if not nums:
        return []

    # Boyer-Moore Majority Vote algorithm for n/3
    candidate1 = candidate2 = None
    count1 = count2 = 0

    # First pass: find potential candidates
    for num in nums:
        if candidate1 == num:
            count1 += 1
        elif candidate2 == num:
            count2 += 1
        elif count1 == 0:
            candidate1, count1 = num, 1
        elif count2 == 0:
            candidate2, count2 = num, 1
        else:
            count1 -= 1
            count2 -= 1

    # Second pass: verify candidates
    result = []
    threshold = len(nums) // 3

    for candidate in [candidate1, candidate2]:
        if candidate is not None and nums.count(candidate) > threshold:
            result.append(candidate)

    return result


def next_greater_elements(nums: list[int]) -> list[int]:
    """Find next greater element for each element (circular array).

    Time: O(n), Space: O(n)

    Args:
        nums: Input array (treated as circular)

    Returns:
        Next greater element for each position

    Examples:
        >>> next_greater_elements([1, 2, 1])
        [2, -1, 2]
        >>> next_greater_elements([1, 2, 3, 4, 3])
        [2, 3, 4, -1, 4]
    """
    if not nums:
        return []

    n = len(nums)
    result = [-1] * n
    stack = []  # Stack to store indices

    # Process array twice to handle circular nature
    for i in range(2 * n):
        current_idx = i % n

        # While stack is not empty and current element is greater than stack top element
        while stack and nums[stack[-1]] < nums[current_idx]:
            idx = stack.pop()
            result[idx] = nums[current_idx]

        # Only add indices from first pass
        if i < n:
            stack.append(i)

    return result


def monotonic_array_check(nums: list[int]) -> bool:
    """Check if array is monotonic (all increasing or all decreasing).

    Time: O(n), Space: O(1)

    Args:
        nums: Array to check

    Returns:
        True if monotonic

    Examples:
        >>> monotonic_array_check([1, 2, 2, 3])
        True
        >>> monotonic_array_check([6, 5, 4, 4])
        True
        >>> monotonic_array_check([1, 3, 2])
        False
    """
    if len(nums) <= 1:
        return True

    increasing = decreasing = True

    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            decreasing = False
        elif nums[i] < nums[i - 1]:
            increasing = False

        # Early termination if neither monotonic property holds
        if not increasing and not decreasing:
            return False

    return True

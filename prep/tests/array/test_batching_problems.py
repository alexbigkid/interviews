"""Tests for batching and array processing problems."""

from src.array.batching_problems import (
    batch_process,
    sliding_window_maximum,
    sliding_window_minimum,
    longest_subarray_sum_k,
    min_subarray_sum_target,
    frequency_based_batching,
    balanced_batching,
    time_window_batching,
    circular_array_rotation,
    interleave_arrays,
    find_duplicates_linear,
    majority_element_n3,
    next_greater_elements,
    monotonic_array_check,
)


class TestBatchProcess:
    """Test batch_process function."""

    def test_simple_batching(self):
        result = batch_process([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_exact_division(self):
        result = batch_process([1, 2, 3, 4], 2)
        assert result == [[1, 2], [3, 4]]

    def test_single_batch(self):
        result = batch_process(["a", "b", "c", "d"], 5)
        assert result == [["a", "b", "c", "d"]]

    def test_empty_input(self):
        result = batch_process([], 2)
        assert result == []

    def test_batch_size_one(self):
        result = batch_process([1, 2, 3], 1)
        assert result == [[1], [2], [3]]

    def test_string_elements(self):
        result = batch_process(["a", "b", "c", "d"], 3)
        assert result == [["a", "b", "c"], ["d"]]


class TestSlidingWindowMaximum:
    """Test sliding_window_maximum function."""

    def test_simple_case(self):
        result = sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)
        assert result == [3, 3, 5, 5, 6, 7]

    def test_single_element_window(self):
        result = sliding_window_maximum([1], 1)
        assert result == [1]

    def test_window_size_one(self):
        result = sliding_window_maximum([1, -1], 1)
        assert result == [1, -1]

    def test_increasing_sequence(self):
        result = sliding_window_maximum([1, 2, 3, 4, 5], 3)
        assert result == [3, 4, 5]

    def test_decreasing_sequence(self):
        result = sliding_window_maximum([5, 4, 3, 2, 1], 3)
        assert result == [5, 4, 3]


class TestSlidingWindowMinimum:
    """Test sliding_window_minimum function."""

    def test_simple_case(self):
        result = sliding_window_minimum([1, 3, -1, -3, 5, 3, 6, 7], 3)
        assert result == [-1, -3, -3, -3, 3, 3]

    def test_single_element_window(self):
        result = sliding_window_minimum([1], 1)
        assert result == [1]

    def test_increasing_sequence(self):
        result = sliding_window_minimum([1, 2, 3, 4, 5], 3)
        assert result == [1, 2, 3]

    def test_decreasing_sequence(self):
        result = sliding_window_minimum([5, 4, 3, 2, 1], 3)
        assert result == [3, 2, 1]


class TestLongestSubarraySumK:
    """Test longest_subarray_sum_k function."""

    def test_simple_case(self):
        assert longest_subarray_sum_k([1, -1, 5, -2, 3], 3) == 4

    def test_multiple_elements_match(self):
        assert longest_subarray_sum_k([1, 1, 1], 2) == 2

    def test_no_match(self):
        assert longest_subarray_sum_k([1, 2, 3], 10) == 0

    def test_negative_numbers(self):
        assert longest_subarray_sum_k([-1, -2, 1, 2], 0) >= 2

    def test_zero_sum(self):
        assert longest_subarray_sum_k([1, -1, 2, -2], 0) >= 2


class TestMinSubarraySumTarget:
    """Test min_subarray_sum_target function."""

    def test_simple_case(self):
        assert min_subarray_sum_target(7, [2, 3, 1, 2, 4, 3]) == 2

    def test_single_element_sufficient(self):
        assert min_subarray_sum_target(4, [1, 4, 4]) == 1

    def test_impossible_case(self):
        assert min_subarray_sum_target(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0

    def test_entire_array_needed(self):
        assert min_subarray_sum_target(15, [1, 2, 3, 4, 5]) == 5

    def test_target_zero(self):
        assert min_subarray_sum_target(0, [1, 2, 3]) == 0


class TestFrequencyBasedBatching:
    """Test frequency_based_batching function."""

    def test_simple_case(self):
        result = frequency_based_batching(["a", "b", "a", "c", "a", "b"], 2)
        # Most frequent 'a' should be in first batches
        assert len(result) == 3
        assert all(len(batch) <= 2 for batch in result)

    def test_all_unique(self):
        result = frequency_based_batching(["a", "b", "c", "d"], 2)
        assert len(result) == 2
        assert all(len(batch) <= 2 for batch in result)

    def test_single_item(self):
        result = frequency_based_batching(["a"], 3)
        assert result == [["a"]]

    def test_empty_input(self):
        result = frequency_based_batching([], 2)
        assert result == []


class TestBalancedBatching:
    """Test balanced_batching function."""

    def test_simple_case(self):
        items = [("a", 3), ("b", 2), ("c", 4), ("d", 1)]
        result = balanced_batching(items, 5)
        assert len(result) == 2
        assert sum(weight for _, weight in result[0]) <= 5
        assert sum(weight for _, weight in result[1]) <= 5

    def test_single_heavy_item(self):
        items = [("a", 10)]
        result = balanced_batching(items, 5)
        # Should handle gracefully even if item exceeds max weight
        assert len(result) >= 1

    def test_all_fit_in_one_batch(self):
        items = [("a", 1), ("b", 1), ("c", 1)]
        result = balanced_batching(items, 5)
        assert len(result) == 1
        assert len(result[0]) == 3

    def test_empty_input(self):
        result = balanced_batching([], 5)
        assert result == []


class TestTimeWindowBatching:
    """Test time_window_batching function."""

    def test_simple_case(self):
        events = [(1, "a"), (2, "b"), (5, "c"), (6, "d")]
        result = time_window_batching(events, 3)
        assert len(result) == 2
        assert (1, "a") in result[0] and (2, "b") in result[0]
        assert (5, "c") in result[1] and (6, "d") in result[1]

    def test_single_event(self):
        events = [(1, "a")]
        result = time_window_batching(events, 5)
        assert result == [[(1, "a")]]

    def test_no_overlapping_windows(self):
        events = [(1, "a"), (10, "b"), (20, "c")]
        result = time_window_batching(events, 3)
        assert len(result) == 3

    def test_empty_input(self):
        result = time_window_batching([], 5)
        assert result == []


class TestCircularArrayRotation:
    """Test circular_array_rotation function."""

    def test_simple_rotation(self):
        result = circular_array_rotation([1, 2, 3, 4, 5, 6, 7], 3)
        assert result == [5, 6, 7, 1, 2, 3, 4]

    def test_rotation_larger_than_length(self):
        result = circular_array_rotation([-1, -100, 3, 99], 2)
        assert result == [3, 99, -1, -100]

    def test_zero_rotation(self):
        result = circular_array_rotation([1, 2, 3], 0)
        assert result == [1, 2, 3]

    def test_full_rotation(self):
        result = circular_array_rotation([1, 2, 3], 3)
        assert result == [1, 2, 3]

    def test_single_element(self):
        result = circular_array_rotation([1], 5)
        assert result == [1]


class TestInterleaveArrays:
    """Test interleave_arrays function."""

    def test_equal_length(self):
        result = interleave_arrays([1, 3, 5], [2, 4, 6])
        assert result == [1, 2, 3, 4, 5, 6]

    def test_first_longer(self):
        result = interleave_arrays(["a", "c"], ["b", "d", "e"])
        assert result == ["a", "b", "c", "d", "e"]

    def test_second_longer(self):
        result = interleave_arrays([1, 2, 3], [4, 5])
        assert result == [1, 4, 2, 5, 3]

    def test_empty_arrays(self):
        result = interleave_arrays([], [1, 2, 3])
        assert result == [1, 2, 3]

    def test_both_empty(self):
        result = interleave_arrays([], [])
        assert result == []


class TestFindDuplicatesLinear:
    """Test find_duplicates_linear function."""

    def test_simple_case(self):
        result = find_duplicates_linear([4, 3, 2, 7, 8, 2, 3, 1])
        assert sorted(result) == [2, 3]

    def test_single_duplicate(self):
        result = find_duplicates_linear([1, 1, 2])
        assert result == [1]

    def test_no_duplicates(self):
        result = find_duplicates_linear([1])
        assert result == []

    def test_multiple_duplicates(self):
        result = find_duplicates_linear([1, 1, 2, 2, 3])
        assert sorted(result) == [1, 2]


class TestMajorityElementN3:
    """Test majority_element_n3 function."""

    def test_single_majority(self):
        result = majority_element_n3([3, 2, 3])
        assert result == [3]

    def test_single_element(self):
        result = majority_element_n3([1])
        assert result == [1]

    def test_two_elements(self):
        result = majority_element_n3([1, 2])
        assert sorted(result) == [1, 2]

    def test_no_majority(self):
        result = majority_element_n3([1, 2, 3, 4, 5, 6])
        assert result == []

    def test_multiple_majorities(self):
        result = majority_element_n3([1, 1, 1, 2, 2, 2, 3])
        assert sorted(result) == [1, 2]


class TestNextGreaterElements:
    """Test next_greater_elements function."""

    def test_simple_case(self):
        result = next_greater_elements([1, 2, 1])
        assert result == [2, -1, 2]

    def test_complex_case(self):
        result = next_greater_elements([1, 2, 3, 4, 3])
        assert result == [2, 3, 4, -1, 4]

    def test_increasing_sequence(self):
        result = next_greater_elements([1, 2, 3, 4, 5])
        assert result == [2, 3, 4, 5, -1]

    def test_single_element(self):
        result = next_greater_elements([1])
        assert result == [-1]


class TestMonotonicArrayCheck:
    """Test monotonic_array_check function."""

    def test_increasing_monotonic(self):
        assert monotonic_array_check([1, 2, 2, 3])

    def test_decreasing_monotonic(self):
        assert monotonic_array_check([6, 5, 4, 4])

    def test_not_monotonic(self):
        assert not monotonic_array_check([1, 3, 2])

    def test_single_element(self):
        assert monotonic_array_check([1])

    def test_all_same(self):
        assert monotonic_array_check([1, 1, 1])

    def test_two_elements_increasing(self):
        assert monotonic_array_check([1, 2])

    def test_two_elements_decreasing(self):
        assert monotonic_array_check([2, 1])

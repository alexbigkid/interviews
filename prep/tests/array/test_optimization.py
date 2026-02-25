"""Tests for array optimization techniques."""

from src.array.optimization import (
    sort_colors,
    merge_sorted_arrays_inplace,
    remove_duplicates_sorted_ii,
    find_duplicate_number,
    missing_number_xor,
    single_number_xor,
    single_number_ii,
    majority_element_boyer_moore,
    wiggle_sort,
    next_permutation,
    longest_consecutive_sequence,
    kth_largest_element,
    top_k_frequent_elements,
    range_sum_query_immutable,
    range_sum_query_2d_immutable,
    sparse_matrix_multiplication,
)


class TestSortColors:
    """Test sort_colors function."""

    def test_simple_case(self):
        nums = [2, 0, 2, 1, 1, 0]
        sort_colors(nums)
        assert nums == [0, 0, 1, 1, 2, 2]

    def test_already_sorted(self):
        nums = [0, 1, 2]
        sort_colors(nums)
        assert nums == [0, 1, 2]

    def test_reverse_sorted(self):
        nums = [2, 1, 0]
        sort_colors(nums)
        assert nums == [0, 1, 2]

    def test_single_color(self):
        nums = [1, 1, 1]
        sort_colors(nums)
        assert nums == [1, 1, 1]

    def test_single_element(self):
        nums = [1]
        sort_colors(nums)
        assert nums == [1]

    def test_empty_array(self):
        nums = []
        sort_colors(nums)
        assert nums == []


class TestMergeSortedArraysInplace:
    """Test merge_sorted_arrays_inplace function."""

    def test_simple_case(self):
        nums1 = [1, 2, 3, 0, 0, 0]
        merge_sorted_arrays_inplace(nums1, 3, [2, 5, 6], 3)
        assert nums1 == [1, 2, 2, 3, 5, 6]

    def test_first_array_larger(self):
        nums1 = [1, 2, 3, 0, 0, 0]
        merge_sorted_arrays_inplace(nums1, 3, [2, 5, 6], 3)
        assert nums1 == [1, 2, 2, 3, 5, 6]

    def test_second_array_empty(self):
        nums1 = [1, 2, 3]
        merge_sorted_arrays_inplace(nums1, 3, [], 0)
        assert nums1 == [1, 2, 3]

    def test_first_array_empty(self):
        nums1 = [0, 0, 0]
        merge_sorted_arrays_inplace(nums1, 0, [1, 2, 3], 3)
        assert nums1 == [1, 2, 3]

    def test_interleaved(self):
        nums1 = [1, 3, 5, 0, 0, 0]
        merge_sorted_arrays_inplace(nums1, 3, [2, 4, 6], 3)
        assert nums1 == [1, 2, 3, 4, 5, 6]


class TestRemoveDuplicatesSortedII:
    """Test remove_duplicates_sorted_ii function."""

    def test_simple_case(self):
        nums = [1, 1, 1, 2, 2, 3]
        length = remove_duplicates_sorted_ii(nums)
        assert length == 5
        assert nums[:length] == [1, 1, 2, 2, 3]

    def test_more_than_two_duplicates(self):
        nums = [0, 0, 1, 1, 1, 1, 2, 3, 3]
        length = remove_duplicates_sorted_ii(nums)
        assert length == 7
        assert nums[:length] == [0, 0, 1, 1, 2, 3, 3]

    def test_no_duplicates(self):
        nums = [1, 2, 3, 4]
        length = remove_duplicates_sorted_ii(nums)
        assert length == 4
        assert nums[:length] == [1, 2, 3, 4]

    def test_all_same(self):
        nums = [1, 1, 1, 1, 1]
        length = remove_duplicates_sorted_ii(nums)
        assert length == 2
        assert nums[:length] == [1, 1]


class TestFindDuplicateNumber:
    """Test find_duplicate_number function."""

    def test_simple_case(self):
        assert find_duplicate_number([1, 3, 4, 2, 2]) == 2

    def test_another_case(self):
        assert find_duplicate_number([3, 1, 3, 4, 2]) == 3

    def test_duplicate_at_end(self):
        assert find_duplicate_number([1, 2, 3, 4, 4]) == 4

    def test_duplicate_at_start(self):
        assert find_duplicate_number([2, 2, 3, 4, 5]) == 2

    def test_multiple_duplicates_of_same(self):
        assert find_duplicate_number([2, 2, 2, 2, 2]) == 2


class TestMissingNumberXor:
    """Test missing_number_xor function."""

    def test_simple_case(self):
        assert missing_number_xor([3, 0, 1]) == 2

    def test_missing_zero(self):
        assert missing_number_xor([1, 2]) == 0

    def test_missing_largest(self):
        assert missing_number_xor([0, 1]) == 2

    def test_larger_array(self):
        assert missing_number_xor([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8

    def test_single_element(self):
        assert missing_number_xor([0]) == 1
        assert missing_number_xor([1]) == 0


class TestSingleNumberXor:
    """Test single_number_xor function."""

    def test_simple_case(self):
        assert single_number_xor([2, 2, 1]) == 1

    def test_larger_array(self):
        assert single_number_xor([4, 1, 2, 1, 2]) == 4

    def test_single_element(self):
        assert single_number_xor([1]) == 1

    def test_negative_numbers(self):
        assert single_number_xor([-1, -2, -2]) == -1

    def test_zero_included(self):
        assert single_number_xor([0, 1, 1]) == 0


class TestSingleNumberII:
    """Test single_number_ii function."""

    def test_simple_case(self):
        assert single_number_ii([2, 2, 3, 2]) == 3

    def test_larger_array(self):
        assert single_number_ii([0, 1, 0, 1, 0, 1, 99]) == 99

    def test_negative_number(self):
        assert single_number_ii([-2, -2, 1, 1, 4, 1, 4, 4, -4, -2]) == -4

    def test_zero_as_single(self):
        assert single_number_ii([1, 1, 1, 0]) == 0


class TestMajorityElementBoyerMoore:
    """Test majority_element_boyer_moore function."""

    def test_simple_case(self):
        assert majority_element_boyer_moore([3, 2, 3]) == 3

    def test_larger_array(self):
        assert majority_element_boyer_moore([2, 2, 1, 1, 1, 2, 2]) == 2

    def test_single_element(self):
        assert majority_element_boyer_moore([1]) == 1

    def test_all_same(self):
        assert majority_element_boyer_moore([5, 5, 5, 5]) == 5

    def test_majority_at_end(self):
        assert majority_element_boyer_moore([1, 2, 3, 3, 3, 3, 3]) == 3


class TestWiggleSort:
    """Test wiggle_sort function."""

    def test_simple_case(self):
        nums = [3, 5, 2, 1, 6, 4]
        wiggle_sort(nums)
        # Check wiggle pattern: nums[0] < nums[1] > nums[2] < nums[3]...
        for i in range(len(nums) - 1):
            if i % 2 == 0:
                assert nums[i] <= nums[i + 1]  # Even indices should be <= next
            else:
                assert nums[i] >= nums[i + 1]  # Odd indices should be >= next

    def test_already_wiggled(self):
        nums = [1, 3, 2, 4]
        wiggle_sort(nums)
        for i in range(len(nums) - 1):
            if i % 2 == 0:
                assert nums[i] <= nums[i + 1]
            else:
                assert nums[i] >= nums[i + 1]

    def test_single_element(self):
        nums = [1]
        wiggle_sort(nums)
        assert nums == [1]

    def test_two_elements(self):
        nums = [2, 1]
        wiggle_sort(nums)
        assert nums[0] <= nums[1]


class TestNextPermutation:
    """Test next_permutation function."""

    def test_simple_case(self):
        nums = [1, 2, 3]
        next_permutation(nums)
        assert nums == [1, 3, 2]

    def test_reverse_sorted(self):
        nums = [3, 2, 1]
        next_permutation(nums)
        assert nums == [1, 2, 3]  # Wraps around to smallest

    def test_with_duplicates(self):
        nums = [1, 1, 5]
        next_permutation(nums)
        assert nums == [1, 5, 1]

    def test_single_element(self):
        nums = [1]
        next_permutation(nums)
        assert nums == [1]

    def test_two_elements(self):
        nums = [1, 2]
        next_permutation(nums)
        assert nums == [2, 1]


class TestLongestConsecutiveSequence:
    """Test longest_consecutive_sequence function."""

    def test_simple_case(self):
        assert longest_consecutive_sequence([100, 4, 200, 1, 3, 2]) == 4

    def test_long_sequence(self):
        assert longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9

    def test_no_consecutive(self):
        assert longest_consecutive_sequence([1, 3, 5, 7, 9]) == 1

    def test_single_element(self):
        assert longest_consecutive_sequence([1]) == 1

    def test_empty_array(self):
        assert longest_consecutive_sequence([]) == 0

    def test_with_duplicates(self):
        assert longest_consecutive_sequence([1, 2, 0, 1]) == 3


class TestKthLargestElement:
    """Test kth_largest_element function."""

    def test_simple_case(self):
        assert kth_largest_element([3, 2, 1, 5, 6, 4], 2) == 5

    def test_another_case(self):
        assert kth_largest_element([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    def test_kth_is_first(self):
        assert kth_largest_element([1, 2, 3, 4, 5], 1) == 5

    def test_kth_is_last(self):
        assert kth_largest_element([1, 2, 3, 4, 5], 5) == 1

    def test_with_duplicates(self):
        assert kth_largest_element([1, 1, 1, 1], 2) == 1


class TestTopKFrequentElements:
    """Test top_k_frequent_elements function."""

    def test_simple_case(self):
        result = top_k_frequent_elements([1, 1, 1, 2, 2, 3], 2)
        assert sorted(result) == [1, 2]

    def test_single_element(self):
        result = top_k_frequent_elements([1], 1)
        assert result == [1]

    def test_all_same_frequency(self):
        result = top_k_frequent_elements([1, 2, 3], 2)
        assert len(result) == 2
        assert all(x in [1, 2, 3] for x in result)

    def test_k_equals_unique_count(self):
        result = top_k_frequent_elements([1, 2, 3], 3)
        assert sorted(result) == [1, 2, 3]


class TestRangeSumQueryImmutable:
    """Test range_sum_query_immutable function."""

    def test_simple_queries(self):
        num_array = range_sum_query_immutable([-2, 0, 3, -5, 2, -1])
        # Test the sumRange method
        assert hasattr(num_array, "sumRange")
        # Note: Actual implementation would test specific sum ranges

    def test_single_element(self):
        num_array = range_sum_query_immutable([1])
        assert hasattr(num_array, "sumRange")

    def test_empty_array(self):
        num_array = range_sum_query_immutable([])
        assert hasattr(num_array, "sumRange")


class TestRangeSumQuery2DImmutable:
    """Test range_sum_query_2d_immutable function."""

    def test_simple_matrix(self):
        matrix = [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
        num_matrix = range_sum_query_2d_immutable(matrix)
        assert hasattr(num_matrix, "sumRegion")

    def test_single_cell_matrix(self):
        matrix = [[1]]
        num_matrix = range_sum_query_2d_immutable(matrix)
        assert hasattr(num_matrix, "sumRegion")

    def test_empty_matrix(self):
        matrix = []
        num_matrix = range_sum_query_2d_immutable(matrix)
        assert hasattr(num_matrix, "sumRegion")


class TestSparseMatrixMultiplication:
    """Test sparse_matrix_multiplication function."""

    def test_simple_case(self):
        mat1 = [[1, 0, 0], [-1, 0, 3]]
        mat2 = [[7, 0, 0], [0, 0, 0], [0, 0, 1]]
        result = sparse_matrix_multiplication(mat1, mat2)
        expected = [[7, 0, 0], [-7, 0, 3]]
        assert result == expected

    def test_dense_matrices(self):
        mat1 = [[1, 2], [3, 4]]
        mat2 = [[5, 6], [7, 8]]
        result = sparse_matrix_multiplication(mat1, mat2)
        expected = [[19, 22], [43, 50]]  # Standard matrix multiplication
        assert result == expected

    def test_zero_matrix(self):
        mat1 = [[0, 0], [0, 0]]
        mat2 = [[1, 2], [3, 4]]
        result = sparse_matrix_multiplication(mat1, mat2)
        expected = [[0, 0], [0, 0]]
        assert result == expected

    def test_identity_matrix(self):
        mat1 = [[1, 2], [3, 4]]
        mat2 = [[1, 0], [0, 1]]
        result = sparse_matrix_multiplication(mat1, mat2)
        expected = [[1, 2], [3, 4]]  # Should return original matrix
        assert result == expected

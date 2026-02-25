"""Tests for basic array operations."""

from src.array.basic_operations import (
    two_sum,
    three_sum,
    container_with_most_water,
    remove_duplicates_sorted,
    remove_element,
    move_zeros,
    find_pivot_index,
    running_sum,
    max_subarray_sum,
    buy_sell_stock,
    product_except_self,
    search_rotated_sorted,
    find_minimum_rotated,
)


class TestTwoSum:
    """Test two_sum function."""

    def test_simple_case(self):
        """Test simple case."""
        result = two_sum([2, 7, 11, 15], 9)
        assert sorted(result) == [0, 1]

    def test_different_order(self):
        """Test different order."""
        result = two_sum([3, 2, 4], 6)
        assert sorted(result) == [1, 2]

    def test_same_elements(self):
        """Test same elements."""
        result = two_sum([3, 3], 6)
        assert sorted(result) == [0, 1]

    def test_negative_numbers(self):
        """Test negative numbers."""
        nums = [-1, -2, -3, -4, -5]
        result = two_sum(nums, -8)
        assert len(result) == 2
        assert result[0] != result[1]
        assert nums[result[0]] + nums[result[1]] == -8
        assert sorted(result) == [2, 4]

    def test_zero_target(self):
        """Test zero target."""
        result = two_sum([-1, 0, 1, 2], 0)
        assert len(result) == 2


class TestThreeSum:
    """Test three_sum function."""

    def test_simple_case(self):
        """Test simple case."""
        result = three_sum([-1, 0, 1, 2, -1, -4])
        expected = [[-1, -1, 2], [-1, 0, 1]]
        assert len(result) == 2
        for triplet in expected:
            assert triplet in result

    def test_no_solution(self):
        """Test no solution case."""
        result = three_sum([0, 1, 1])
        assert result == []

    def test_all_zeros(self):
        """Test all zeros case."""
        result = three_sum([0, 0, 0])
        assert result == [[0, 0, 0]]

    def test_single_solution(self):
        """Test single solution case."""
        result = three_sum([-2, 0, 1, 1, 2])
        assert [-2, 0, 2] in result or [-2, 1, 1] in result

    def test_duplicates_handling(self):
        """Test handling of duplicates."""
        result = three_sum([-1, 0, 1, 2, -1, -4])
        # Should not have duplicate triplets
        unique_triplets = set(tuple(sorted(triplet)) for triplet in result)
        assert len(unique_triplets) == len(result)


class TestContainerWithMostWater:
    """Test container_with_most_water function."""

    def test_simple_case(self):
        """Test simple case."""
        assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    def test_two_elements(self):
        """Test two elements case."""
        assert container_with_most_water([1, 1]) == 1

    def test_increasing_heights(self):
        """Test increasing heights case."""
        assert container_with_most_water([1, 2, 3, 4, 5]) == 6

    def test_decreasing_heights(self):
        """Test decreasing heights case."""
        assert container_with_most_water([5, 4, 3, 2, 1]) == 6

    def test_tall_edges(self):
        """Test tall edges case."""
        assert container_with_most_water([4, 3, 2, 1, 4]) == 16


class TestRemoveDuplicatesSorted:
    """Test remove_duplicates_sorted function."""

    def test_simple_case(self):
        """Test simple case."""
        nums = [1, 1, 2]
        length = remove_duplicates_sorted(nums)
        assert length == 2
        assert nums[:length] == [1, 2]

    def test_no_duplicates(self):
        """Test no duplicates case."""
        nums = [1, 2, 3, 4, 5]
        length = remove_duplicates_sorted(nums)
        assert length == 5
        assert nums[:length] == [1, 2, 3, 4, 5]

    def test_all_same(self):
        """Test all elements the same case."""
        nums = [1, 1, 1, 1]
        length = remove_duplicates_sorted(nums)
        assert length == 1
        assert nums[:length] == [1]

    def test_empty_array(self):
        """Test empty array case."""
        nums = []
        length = remove_duplicates_sorted(nums)
        assert length == 0

    def test_single_element(self):
        """Test single element case."""
        nums = [1]
        length = remove_duplicates_sorted(nums)
        assert length == 1
        assert nums[:length] == [1]


class TestRemoveElement:
    """Test remove_element function."""

    def test_simple_case(self):
        """Test simple case."""
        nums = [3, 2, 2, 3]
        length = remove_element(nums, 3)
        assert length == 2
        assert sorted(nums[:length]) == [2, 2]

    def test_remove_all(self):
        """Test removing all elements."""
        nums = [1, 1, 1, 1]
        length = remove_element(nums, 1)
        assert length == 0

    def test_remove_none(self):
        """Test removing no elements."""
        nums = [1, 2, 3, 4]
        length = remove_element(nums, 5)
        assert length == 4

    def test_empty_array(self):
        """Test empty array case."""
        nums = []
        length = remove_element(nums, 1)
        assert length == 0


class TestMoveZeros:
    """Test move_zeros function."""

    def test_simple_case(self):
        """Test simple case."""
        nums = [0, 1, 0, 3, 12]
        move_zeros(nums)
        assert nums == [1, 3, 12, 0, 0]

    def test_no_zeros(self):
        """Test no zeros case."""
        nums = [1, 2, 3, 4, 5]
        move_zeros(nums)
        assert nums == [1, 2, 3, 4, 5]
        nums = [1, 2, 3, 4, 5]
        move_zeros(nums)
        assert nums == [1, 2, 3, 4, 5]

    def test_all_zeros(self):
        """Test all zeros case."""
        nums = [0, 0, 0, 0]
        move_zeros(nums)
        assert nums == [0, 0, 0, 0]

    def test_zeros_at_end(self):
        """Test zeros at end case."""
        nums = [1, 2, 3, 0, 0]
        nums = [1, 2, 3, 0, 0]
        move_zeros(nums)
        assert nums == [1, 2, 3, 0, 0]

    def test_single_element(self):
        """Test single element case."""
        nums = [0]
        move_zeros(nums)
        assert nums == [0]


class TestFindPivotIndex:
    """Test find_pivot_index function."""

    def test_simple_case(self):
        """Test simple case."""
        assert find_pivot_index([1, 7, 3, 6, 5, 6]) == 3

    def test_no_pivot(self):
        """Test no pivot case."""
        assert find_pivot_index([1, 2, 3]) == -1

    def test_pivot_at_start(self):
        """Test pivot at start case."""
        assert find_pivot_index([2, 1, -1]) == 0

    def test_pivot_at_end(self):
        """Test pivot at end case."""
        assert find_pivot_index([-1, 1, 2]) == 2

    def test_single_element(self):
        """Test single element case."""
        assert find_pivot_index([1]) == 0

    def test_all_zeros(self):
        """Test all zeros case."""
        assert find_pivot_index([0, 0, 0]) == 0


class TestRunningSum:
    """Test running_sum function."""

    def test_simple_case(self):
        """Test simple case with basic input."""
        assert running_sum([1, 2, 3, 4]) == [1, 3, 6, 10]

    def test_all_ones(self):
        """Test with all ones."""
        assert running_sum([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]

    def test_mixed_numbers(self):
        """Test with mixed positive numbers."""
        assert running_sum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]

    def test_negative_numbers(self):
        """Test with negative numbers."""
        assert running_sum([-1, -2, -3]) == [-1, -3, -6]

    def test_single_element(self):
        """Test with single element array."""
        assert running_sum([5]) == [5]

    def test_zeros(self):
        """Test with all zeros."""
        assert running_sum([0, 0, 0]) == [0, 0, 0]


class TestMaxSubarraySum:
    """Test max_subarray_sum function."""

    def test_kadane_example(self):
        """Test classic Kadane's algorithm example."""
        assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

    def test_single_element(self):
        """Test with single element arrays."""
        assert max_subarray_sum([1]) == 1
        assert max_subarray_sum([-1]) == -1

    def test_all_positive(self):
        """Test with mostly positive numbers."""
        assert max_subarray_sum([5, 4, -1, 7, 8]) == 23

    def test_all_negative(self):
        """Test with all negative numbers."""
        assert max_subarray_sum([-3, -2, -1, -4]) == -1

    def test_mixed_with_zeros(self):
        """Test with mixed numbers including zeros."""
        assert max_subarray_sum([0, -1, 2, -1, 3]) == 4


class TestBuySellStock:
    """Test buy_sell_stock function."""

    def test_simple_case(self):
        """Test simple case with profit opportunity."""
        assert buy_sell_stock([7, 1, 5, 3, 6, 4]) == 5

    def test_decreasing_prices(self):
        """Test with continuously decreasing prices."""
        assert buy_sell_stock([7, 6, 4, 3, 1]) == 0

    def test_increasing_prices(self):
        """Test with continuously increasing prices."""
        assert buy_sell_stock([1, 2, 3, 4, 5]) == 4

    def test_single_price(self):
        """Test with single price (no transaction possible)."""
        assert buy_sell_stock([1]) == 0

    def test_two_prices(self):
        """Test with two prices for profit and loss scenarios."""
        assert buy_sell_stock([1, 5]) == 4
        assert buy_sell_stock([5, 1]) == 0


class TestProductExceptSelf:
    """Test product_except_self function."""

    def test_simple_case(self):
        """Test simple case with basic input."""
        assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]

    def test_with_zero(self):
        """Test with zero in the array."""
        assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    def test_negative_numbers(self):
        """Test with negative numbers."""
        result = product_except_self([-1, -2, -3])
        assert result == [6, 3, 2]

    def test_single_element(self):
        """Test with single element array."""
        assert product_except_self([5]) == [1]

    def test_with_ones(self):
        """Test with all ones."""
        assert product_except_self([1, 1, 1, 1]) == [1, 1, 1, 1]


class TestSearchRotatedSorted:
    """Test search_rotated_sorted function."""

    def test_target_found(self):
        """Test when target is found in rotated array."""
        assert search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 0) == 4

    def test_target_not_found(self):
        """Test when target is not found in rotated array."""
        assert search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 3) == -1

    def test_single_element_found(self):
        """Test with single element array where target is found."""
        assert search_rotated_sorted([1], 1) == 0

    def test_single_element_not_found(self):
        """Test with single element array where target is not found."""
        assert search_rotated_sorted([1], 0) == -1

    def test_no_rotation(self):
        """Test with no rotation (normal sorted array)."""
        assert search_rotated_sorted([1, 2, 3, 4, 5], 3) == 2

    def test_target_at_rotation_point(self):
        """Test when target is at the rotation point."""
        assert search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 4) == 0


class TestFindMinimumRotated:
    """Test find_minimum_rotated function."""

    def test_rotated_array(self):
        """Test with rotated array."""
        assert find_minimum_rotated([3, 4, 5, 1, 2]) == 1

    def test_another_rotation(self):
        """Test with another rotation example."""
        assert find_minimum_rotated([4, 5, 6, 7, 0, 1, 2]) == 0

    def test_no_rotation(self):
        """Test with no rotation (normal sorted array)."""
        assert find_minimum_rotated([11, 13, 15, 17]) == 11

    def test_single_element(self):
        """Test with single element array."""
        assert find_minimum_rotated([1]) == 1

    def test_two_elements(self):
        """Test with two element arrays."""
        assert find_minimum_rotated([2, 1]) == 1
        assert find_minimum_rotated([1, 2]) == 1

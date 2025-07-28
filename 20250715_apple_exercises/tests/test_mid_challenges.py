"""
Unit tests for mid level Python challenges
"""

from abk_apple.mid_challenges import (
    group_anagrams,
    three_sum,
    longest_substring_without_repeating,
    valid_parentheses,
    product_except_self,
    max_subarray,
    rotate_array,
)


class TestGroupAnagrams:
    def test_basic_case(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Sort each group and the result for comparison
        sorted_result = sorted([sorted(group) for group in result])
        expected = sorted([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
        assert sorted_result == expected

    def test_empty_strings(self):
        result = group_anagrams([""])
        assert result == [[""]]

    def test_single_character(self):
        result = group_anagrams(["a"])
        assert result == [["a"]]


class TestThreeSum:
    def test_basic_case(self):
        result = three_sum([-1, 0, 1, 2, -1, -4])
        expected = [[-1, -1, 2], [-1, 0, 1]]
        assert sorted(result) == sorted(expected)

    def test_no_solution(self):
        result = three_sum([0, 1, 1])
        assert result == []

    def test_all_zeros(self):
        result = three_sum([0, 0, 0])
        assert result == [[0, 0, 0]]


class TestLongestSubstringWithoutRepeating:
    def test_basic_case(self):
        assert longest_substring_without_repeating("abcabcbb") == 3

    def test_all_same_characters(self):
        assert longest_substring_without_repeating("bbbbb") == 1

    def test_no_repeating_characters(self):
        assert longest_substring_without_repeating("pwwkew") == 3

    def test_empty_string(self):
        assert longest_substring_without_repeating("") == 0


class TestValidParentheses:
    def test_valid_parentheses(self):
        assert valid_parentheses("()") == True
        assert valid_parentheses("()[]{}") == True
        assert valid_parentheses("([{}])") == True

    def test_invalid_parentheses(self):
        assert valid_parentheses("(]") == False
        assert valid_parentheses("([)]") == False
        assert valid_parentheses("((") == False

    def test_empty_string(self):
        assert valid_parentheses("") == True


class TestProductExceptSelf:
    def test_basic_case(self):
        assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]

    def test_with_zero(self):
        assert product_except_self([0, 1, 2, 3]) == [6, 0, 0, 0]

    def test_negative_numbers(self):
        assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]


class TestMaxSubarray:
    def test_basic_case(self):
        assert max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

    def test_all_negative(self):
        assert max_subarray([-2, -1, -3]) == -1

    def test_single_element(self):
        assert max_subarray([5]) == 5

    def test_all_positive(self):
        assert max_subarray([1, 2, 3, 4, 5]) == 15


class TestRotateArray:
    def test_basic_case(self):
        nums = [1, 2, 3, 4, 5, 6, 7]
        rotate_array(nums, 3)
        assert nums == [5, 6, 7, 1, 2, 3, 4]

    def test_rotate_by_length(self):
        nums = [1, 2, 3]
        rotate_array(nums, 3)
        assert nums == [1, 2, 3]  # No change

    def test_rotate_by_zero(self):
        nums = [1, 2, 3, 4]
        rotate_array(nums, 0)
        assert nums == [1, 2, 3, 4]  # No change

    def test_rotate_large_k(self):
        nums = [1, 2]
        rotate_array(nums, 3)  # k > len(nums)
        assert nums == [2, 1]

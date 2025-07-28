"""
Unit tests for easy level Python challenges
"""

from abk_apple.easy_challenges import (
    two_sum,
    is_palindrome,
    reverse_string,
    fizz_buzz,
    contains_duplicate,
)


class TestTwoSum:
    def test_basic_case(self):
        assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    def test_negative_numbers(self):
        assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]

    def test_zero_target(self):
        assert two_sum([-3, 4, 3, 90], 0) == [0, 2]


class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("A man, a plan, a canal: Panama") == True

    def test_not_palindrome(self):
        assert is_palindrome("race a car") == False

    def test_empty_string(self):
        assert is_palindrome(" ") == True

    def test_single_character(self):
        assert is_palindrome("a") == True


class TestReverseString:
    def test_basic_reverse(self):
        s = ["h", "e", "l", "l", "o"]
        reverse_string(s)
        assert s == ["o", "l", "l", "e", "h"]

    def test_single_character(self):
        s = ["a"]
        reverse_string(s)
        assert s == ["a"]

    def test_two_characters(self):
        s = ["a", "b"]
        reverse_string(s)
        assert s == ["b", "a"]


class TestFizzBuzz:
    def test_basic_case(self):
        assert fizz_buzz(3) == ["1", "2", "Fizz"]

    def test_fizz_buzz_case(self):
        assert fizz_buzz(5) == ["1", "2", "Fizz", "4", "Buzz"]

    def test_fizz_buzz_fifteen(self):
        result = fizz_buzz(15)
        assert result[14] == "FizzBuzz"  # 15th element
        assert result[11] == "Fizz"  # 12th element
        assert result[9] == "Buzz"  # 10th element


class TestContainsDuplicate:
    def test_has_duplicate(self):
        assert contains_duplicate([1, 2, 3, 1]) == True

    def test_no_duplicate(self):
        assert contains_duplicate([1, 2, 3, 4]) == False

    def test_empty_array(self):
        assert contains_duplicate([]) == False

    def test_single_element(self):
        assert contains_duplicate([1]) == False

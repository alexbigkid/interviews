"""Tests for basic string operations."""

import pytest
from src.string.basic_operations import (
    reverse_string,
    reverse_string_inplace,
    rotate_string_left,
    character_frequency,
    most_frequent_character,
    remove_duplicates,
    is_subsequence,
    first_unique_character,
)


class TestReverseString:
    """Test reverse_string function."""

    def test_normal_string(self):
        """Test normal string reversal."""
        assert reverse_string("hello") == "olleh"

    def test_single_character(self):
        """Test single character string reversal."""
        assert reverse_string("a") == "a"

    def test_empty_string(self):
        """Test empty string reversal."""
        assert reverse_string("") == ""

    def test_palindrome(self):
        """Test palindrome string reversal."""
        assert reverse_string("racecar") == "racecar"

    def test_with_spaces(self):
        """Test string with spaces reversal."""
        assert reverse_string("hello world") == "dlrow olleh"


class TestReverseStringInplace:
    """Test reverse_string_inplace function."""

    def test_normal_list(self):
        """Test normal list reversal."""
        chars = ["h", "e", "l", "l", "o"]
        reverse_string_inplace(chars)
        assert chars == ["o", "l", "l", "e", "h"]

    def test_single_character(self):
        """Test single character list reversal."""
        chars = ["a"]
        reverse_string_inplace(chars)
        assert chars == ["a"]

    def test_empty_list(self):
        """Test empty list reversal."""
        chars = []
        reverse_string_inplace(chars)
        assert chars == []

    def test_two_characters(self):
        """Test two character list reversal."""
        chars = ["a", "b"]
        reverse_string_inplace(chars)
        assert chars == ["b", "a"]


class TestRotateStringLeft:
    """Test rotate_string_left function."""

    def test_normal_rotation(self):
        """Test normal string rotation."""
        assert rotate_string_left("abcdef", 2) == "cdefab"

    def test_single_position(self):
        """Test single position rotation."""
        assert rotate_string_left("hello", 1) == "elloh"

    def test_full_rotation(self):
        """Test full rotation."""
        assert rotate_string_left("abc", 3) == "abc"

    def test_larger_than_length(self):
        """Test rotation larger than string length."""
        assert rotate_string_left("abc", 4) == "bca"  # 4 % 3 = 1

    def test_zero_rotation(self):
        """Test zero rotation."""
        assert rotate_string_left("hello", 0) == "hello"

    def test_empty_string(self):
        """Test empty string rotation."""
        assert rotate_string_left("", 5) == ""


class TestCharacterFrequency:
    """Test character_frequency function."""

    def test_normal_string(self):
        """Test normal string frequency."""
        result = character_frequency("hello")
        expected = {"h": 1, "e": 1, "l": 2, "o": 1}
        assert result == expected

    def test_all_same_characters(self):
        """Test string with all same characters."""
        result = character_frequency("aaa")
        assert result == {"a": 3}

    def test_empty_string(self):
        """Test empty string frequency."""
        assert character_frequency("") == {}

    def test_single_character(self):
        """Test single character string frequency."""
        assert character_frequency("a") == {"a": 1}

    def test_with_spaces(self):
        """Test string with spaces frequency."""
        result = character_frequency("a b a")
        expected = {"a": 2, " ": 2, "b": 1}
        assert result == expected


class TestMostFrequentCharacter:
    """Test most_frequent_character function."""

    def test_clear_winner(self):
        """Test string with a clear most frequent character."""
        assert most_frequent_character("hello") == "l"

    def test_tie_returns_first(self):
        """Test string with a tie for most frequent character."""
        assert most_frequent_character("aabbcc") == "a"

    def test_single_character(self):
        """Test single character string."""
        assert most_frequent_character("a") == "a"

    def test_empty_string_raises(self):
        """Test empty string raises ValueError."""
        with pytest.raises(ValueError):
            most_frequent_character("")

    def test_all_unique(self):
        """Test string with all unique characters."""
        assert most_frequent_character("abc") == "a"


class TestRemoveDuplicates:
    """Test remove_duplicates function."""

    def test_normal_string(self):
        """Test normal string removal of duplicates."""
        assert remove_duplicates("hello") == "helo"

    def test_all_duplicates(self):
        """Test string with all same characters."""
        assert remove_duplicates("aaa") == "a"

    def test_no_duplicates(self):
        """Test string with no duplicates."""
        assert remove_duplicates("abc") == "abc"

    def test_empty_string(self):
        """Test empty string removal of duplicates."""
        assert remove_duplicates("") == ""

    def test_single_character(self):
        """Test single character removal of duplicates."""
        assert remove_duplicates("a") == "a"

    def test_complex_pattern(self):
        """Test string with complex pattern of duplicates."""
        assert remove_duplicates("programming") == "progamin"


class TestIsSubsequence:
    """Test is_subsequence function."""

    def test_valid_subsequence(self):
        """Test valid subsequence."""
        assert is_subsequence("ace", "abcde")

    def test_invalid_subsequence(self):
        """Test invalid subsequence."""
        assert not is_subsequence("aec", "abcde")

    def test_empty_subsequence(self):
        """Test empty subsequence."""
        assert is_subsequence("", "abc")

    def test_empty_target(self):
        """Test empty target."""
        assert not is_subsequence("a", "")

    def test_both_empty(self):
        """Test both strings empty."""
        assert is_subsequence("", "")

    def test_same_strings(self):
        """Test identical strings."""
        assert is_subsequence("abc", "abc")

    def test_single_character_match(self):
        """Test single character match."""
        assert is_subsequence("c", "abc")

    def test_single_character_no_match(self):
        """Test single character no match."""
        assert not is_subsequence("d", "abc")


class TestFirstUniqueCharacter:
    """Test first_unique_character function."""

    def test_first_character_unique(self):
        assert first_unique_character("leetcode") == 0

    def test_middle_character_unique(self):
        assert first_unique_character("loveleetcode") == 2

    def test_no_unique_character(self):
        assert first_unique_character("aabb") == -1

    def test_single_character(self):
        assert first_unique_character("a") == 0

    def test_empty_string(self):
        assert first_unique_character("") == -1

    def test_all_same(self):
        assert first_unique_character("aaa") == -1

    def test_last_character_unique(self):
        assert first_unique_character("aabbccd") == 6

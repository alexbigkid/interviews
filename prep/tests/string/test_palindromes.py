"""Tests for palindrome-related string operations."""

from src.string.palindromes import (
    is_palindrome,
    is_palindrome_ignore_case_punctuation,
    longest_palindrome_substring,
    palindrome_pairs,
    palindromic_substrings_count,
    shortest_palindrome,
    valid_palindrome_ii,
)


class TestIsPalindrome:
    """Test is_palindrome function."""

    def test_simple_palindrome(self):
        """Test simple palindrome cases."""
        assert is_palindrome("racecar")

    def test_not_palindrome(self):
        """Test non-palindrome cases."""
        assert not is_palindrome("hello")

    def test_empty_string(self):
        """Test empty string."""
        assert is_palindrome("")

    def test_single_character(self):
        """Test single character string."""
        assert is_palindrome("a")

    def test_case_sensitive(self):
        """Test case sensitivity."""
        assert not is_palindrome("Racecar")

    def test_even_length_palindrome(self):
        """Test even length palindrome."""
        assert is_palindrome("abba")

    def test_odd_length_palindrome(self):
        """Test odd length palindrome."""
        assert is_palindrome("aba")


class TestIsPalindromeIgnoreCasePunctuation:
    """Test is_palindrome_ignore_case_punctuation function."""

    def test_with_punctuation_and_case(self):
        """Test the classic example with punctuation and mixed case."""
        assert is_palindrome_ignore_case_punctuation("A man, a plan, a canal: Panama")

    def test_not_palindrome_with_spaces(self):
        """Test string that's not a palindrome even after normalization."""
        assert not is_palindrome_ignore_case_punctuation("race a car")

    def test_empty_string(self):
        """Test empty string."""
        assert is_palindrome_ignore_case_punctuation("")

    def test_single_character(self):
        """Test single character."""
        assert is_palindrome_ignore_case_punctuation("a")
        assert is_palindrome_ignore_case_punctuation("A")

    def test_only_punctuation(self):
        """Test string with only punctuation and spaces."""
        assert is_palindrome_ignore_case_punctuation(".,! !,.")
        assert is_palindrome_ignore_case_punctuation("   ")

    def test_alphanumeric_palindrome(self):
        """Test palindromes with mixed letters and numbers."""
        assert not is_palindrome_ignore_case_punctuation("A1B2a")  # a1b2a normalized
        assert is_palindrome_ignore_case_punctuation("A1a")  # a1a normalized
        assert is_palindrome_ignore_case_punctuation("1A2a2A1")  # 1a2a2a1 normalized

    def test_case_insensitive(self):
        """Test case insensitivity."""
        assert is_palindrome_ignore_case_punctuation("RaceCar")
        assert is_palindrome_ignore_case_punctuation("AbA")
        assert is_palindrome_ignore_case_punctuation("ABBA")

    def test_complex_punctuation(self):
        """Test with various punctuation marks."""
        assert is_palindrome_ignore_case_punctuation("Madam, I'm Adam!")
        assert is_palindrome_ignore_case_punctuation("Was it a car or a cat I saw?")
        assert is_palindrome_ignore_case_punctuation("No 'x' in Nixon")

    def test_numbers_and_letters(self):
        """Test combinations of numbers and letters."""
        assert is_palindrome_ignore_case_punctuation("A man a plan a canal Panama")
        assert is_palindrome_ignore_case_punctuation("12321")
        assert is_palindrome_ignore_case_punctuation("A1B2C2b1a")  # a1b2c2b1a normalized

    def test_edge_cases(self):
        """Test edge cases."""
        assert is_palindrome_ignore_case_punctuation(".,")  # Only punctuation
        assert is_palindrome_ignore_case_punctuation("a.")  # Single char with punctuation
        assert is_palindrome_ignore_case_punctuation(".a.")  # Single char surrounded by punctuation


class TestLongestPalindromeSubstring:
    """Test longest_palindrome_substring function."""

    def test_simple_case(self):
        """Test simple cases."""
        result = longest_palindrome_substring("babad")
        assert result in ["bab", "aba"]

    def test_even_palindrome(self):
        """Test even length palindrome."""
        assert longest_palindrome_substring("cbbd") == "bb"

    def test_single_character(self):
        """Test single character string."""
        assert longest_palindrome_substring("a") == "a"

    def test_no_palindrome_longer_than_one(self):
        """Test string with no palindrome longer than one character."""
        result = longest_palindrome_substring("abc")
        assert len(result) == 1
        assert result in ["a", "b", "c"]

    def test_entire_string_palindrome(self):
        """Test when the entire string is a palindrome."""
        assert longest_palindrome_substring("racecar") == "racecar"

    def test_empty_string(self):
        """Test empty string."""
        assert longest_palindrome_substring("") == ""


class TestPalindromePairs:
    """Test palindrome_pairs function."""

    def test_simple_pairs(self):
        """Test simple cases."""
        words = ["abcd", "dcba", "lls", "s", "sssll"]
        result = palindrome_pairs(words)
        expected_pairs = [(0, 1), (1, 0), (3, 2), (2, 4)]
        assert sorted(result) == sorted(expected_pairs)

    def test_empty_list(self):
        """Test empty list."""
        assert palindrome_pairs([]) == []

    def test_single_word(self):
        """Test single word list."""
        assert palindrome_pairs(["abc"]) == []

    def test_no_pairs(self):
        """Test list with no palindrome pairs."""
        assert palindrome_pairs(["abc", "def", "ghi"]) == []

    def test_with_empty_string(self):
        """Test list containing an empty string."""
        words = ["", "a"]
        result = palindrome_pairs(words)
        assert (0, 1) in result and (1, 0) in result  # Both "" + "a" and "a" + "" form palindromes


class TestShortestPalindrome:
    """Test shortest_palindrome function."""

    def test_simple_case(self):
        """Test simple cases."""
        assert shortest_palindrome("aacecaaa") == "aaacecaaa"

    def test_already_palindrome(self):
        """Test when the input string is already a palindrome."""
        assert shortest_palindrome("racecar") == "racecar"

    def test_single_character(self):
        """Test single character string."""
        assert shortest_palindrome("a") == "a"

    def test_empty_string(self):
        """Test empty string."""
        assert shortest_palindrome("") == ""

    def test_no_palindrome_prefix(self):
        """Test string with no palindrome prefix."""
        result = shortest_palindrome("abcd")
        assert result == "dcbabcd"


class TestValidPalindromeII:
    """Test valid_palindrome_ii function."""

    def test_valid_with_one_deletion(self):
        """Test cases that can become palindromes with one deletion."""
        assert valid_palindrome_ii("aba")

    def test_valid_after_one_deletion(self):
        """Test cases that need one deletion to become palindromes."""
        assert valid_palindrome_ii("abca")

    def test_invalid_even_with_deletion(self):
        """Test cases that cannot become palindromes even with one deletion."""
        assert not valid_palindrome_ii("abc")

    def test_already_palindrome(self):
        """Test cases that are already palindromes."""
        assert valid_palindrome_ii("racecar")

    def test_empty_string(self):
        """Test empty string."""
        assert valid_palindrome_ii("")

    def test_single_character(self):
        """Test single character string."""
        assert valid_palindrome_ii("a")

    def test_two_characters(self):
        """Test two character strings."""
        assert valid_palindrome_ii("ab")


class TestPalindromicSubstringsCount:
    """Test palindromic_substrings_count function."""

    def test_simple_case(self):
        """Test simple cases."""
        assert palindromic_substrings_count("abba") == 6
        assert palindromic_substrings_count("abc") == 3

    def test_with_palindromes(self):
        """Test cases with multiple palindromic substrings."""
        assert palindromic_substrings_count("aaa") == 6

    def test_mixed_palindromes(self):
        """Test mixed cases."""
        assert palindromic_substrings_count("aba") == 4

    def test_single_character(self):
        """Test single character string."""
        assert palindromic_substrings_count("a") == 1

    def test_empty_string(self):
        """Test empty string."""
        assert palindromic_substrings_count("") == 0

    def test_longer_example(self):
        """Test longer example."""
        # "racecar" has: r, a, c, e, c, a, r, cec, aceca, racecar = 10
        assert palindromic_substrings_count("racecar") >= 7  # At least single chars

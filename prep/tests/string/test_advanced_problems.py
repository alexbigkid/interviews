"""Tests for advanced string algorithm problems."""

from src.string.advanced_problems import (
    edit_distance,
    edit_distance_space_optimized,
    longest_common_subsequence,
    longest_common_substring,
    is_interleaving,
    distinct_subsequences,
    word_break,
    word_break_ii,
    scramble_string,
    minimum_window_with_chars,
    longest_palindrome_subsequence,
    decode_ways,
)


class TestEditDistance:
    """Test edit_distance function."""

    def test_simple_case(self):
        assert edit_distance("horse", "ros") == 3

    def test_complex_case(self):
        assert edit_distance("intention", "execution") == 5

    def test_empty_strings(self):
        assert edit_distance("", "abc") == 3
        assert edit_distance("abc", "") == 3
        assert edit_distance("", "") == 0

    def test_identical_strings(self):
        assert edit_distance("hello", "hello") == 0

    def test_single_character(self):
        assert edit_distance("a", "b") == 1
        assert edit_distance("a", "a") == 0

    def test_one_empty(self):
        assert edit_distance("abc", "") == 3
        assert edit_distance("", "abc") == 3


class TestEditDistanceSpaceOptimized:
    """Test edit_distance_space_optimized function."""

    def test_simple_case(self):
        assert edit_distance_space_optimized("horse", "ros") == 3

    def test_complex_case(self):
        assert edit_distance_space_optimized("intention", "execution") == 5

    def test_empty_strings(self):
        assert edit_distance_space_optimized("", "abc") == 3
        assert edit_distance_space_optimized("abc", "") == 3

    def test_identical_strings(self):
        assert edit_distance_space_optimized("hello", "hello") == 0


class TestLongestCommonSubsequence:
    """Test longest_common_subsequence function."""

    def test_simple_case(self):
        assert longest_common_subsequence("abcde", "ace") == 3

    def test_identical_strings(self):
        assert longest_common_subsequence("abc", "abc") == 3

    def test_no_common_subsequence(self):
        assert longest_common_subsequence("abc", "def") == 0

    def test_empty_strings(self):
        assert longest_common_subsequence("", "abc") == 0
        assert longest_common_subsequence("abc", "") == 0
        assert longest_common_subsequence("", "") == 0

    def test_partial_match(self):
        assert longest_common_subsequence("ABCDGH", "AEDFHR") == 3


class TestLongestCommonSubstring:
    """Test longest_common_substring function."""

    def test_simple_case(self):
        assert longest_common_substring("abcdxyz", "xyzabcd") == 4

    def test_complex_case(self):
        assert longest_common_substring("zxabcdezy", "yzabcdezx") == 6

    def test_no_common_substring(self):
        assert longest_common_substring("abc", "def") == 0

    def test_identical_strings(self):
        assert longest_common_substring("abc", "abc") == 3

    def test_empty_strings(self):
        assert longest_common_substring("", "abc") == 0
        assert longest_common_substring("abc", "") == 0


class TestIsInterleaving:
    """Test is_interleaving function."""

    def test_valid_interleaving(self):
        assert is_interleaving("aabcc", "dbbca", "aadbbcbcac")

    def test_invalid_interleaving(self):
        assert not is_interleaving("aabcc", "dbbca", "aadbbbaccc")

    def test_empty_strings(self):
        assert is_interleaving("", "", "")
        assert is_interleaving("a", "", "a")
        assert is_interleaving("", "b", "b")

    def test_wrong_length(self):
        assert not is_interleaving("ab", "cd", "abcde")

    def test_simple_case(self):
        assert is_interleaving("ab", "cd", "acbd")
        assert is_interleaving("ab", "cd", "abcd")


class TestDistinctSubsequences:
    """Test distinct_subsequences function."""

    def test_simple_case(self):
        assert distinct_subsequences("rabbbit", "rabbit") == 3

    def test_complex_case(self):
        assert distinct_subsequences("babgbag", "bag") == 5

    def test_no_subsequences(self):
        assert distinct_subsequences("abc", "def") == 0

    def test_empty_target(self):
        assert distinct_subsequences("abc", "") == 1

    def test_empty_source(self):
        assert distinct_subsequences("", "abc") == 0

    def test_identical_strings(self):
        assert distinct_subsequences("abc", "abc") == 1


class TestWordBreak:
    """Test word_break function."""

    def test_valid_break(self):
        assert word_break("leetcode", ["leet", "code"])

    def test_multiple_valid_breaks(self):
        assert word_break("applepenapple", ["apple", "pen"])

    def test_invalid_break(self):
        assert not word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])

    def test_empty_string(self):
        assert word_break("", ["a", "b"])

    def test_repeated_usage(self):
        assert word_break("aaaaaaa", ["aaaa", "aaa"])

    def test_single_word(self):
        assert word_break("hello", ["hello"])


class TestWordBreakII:
    """Test word_break_ii function."""

    def test_multiple_solutions(self):
        result = word_break_ii("catsanddog", ["cat", "cats", "and", "sand", "dog"])
        expected = {"cats and dog", "cat sand dog"}
        assert set(result) == expected

    def test_single_solution(self):
        result = word_break_ii("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"])
        assert len(result) > 0

    def test_no_solution(self):
        result = word_break_ii("catsandog", ["cats", "dog", "sand", "and", "cat"])
        assert result == []

    def test_empty_string(self):
        result = word_break_ii("", ["a", "b"])
        assert result == [""]


class TestScrambleString:
    """Test scramble_string function."""

    def test_valid_scramble(self):
        assert scramble_string("great", "rgeat")

    def test_another_valid_scramble(self):
        assert scramble_string("abcdef", "fecabd")

    def test_identical_strings(self):
        assert scramble_string("abc", "abc")

    def test_different_lengths(self):
        assert not scramble_string("abc", "abcd")

    def test_different_characters(self):
        assert not scramble_string("abc", "def")


class TestMinimumWindowWithChars:
    """Test minimum_window_with_chars function."""

    def test_simple_case(self):
        assert minimum_window_with_chars("ADOBECODEBANC", "ABC") == "BANC"

    def test_single_character(self):
        assert minimum_window_with_chars("a", "a") == "a"

    def test_no_valid_window(self):
        assert minimum_window_with_chars("a", "aa") == ""

    def test_entire_string_needed(self):
        assert minimum_window_with_chars("abc", "abc") == "abc"

    def test_repeated_characters(self):
        result = minimum_window_with_chars("ADOBECODEBANC", "AABC")
        assert "A" in result and "B" in result and "C" in result
        assert result.count("A") >= 2


class TestLongestPalindromeSubsequence:
    """Test longest_palindrome_subsequence function."""

    def test_simple_case(self):
        assert longest_palindrome_subsequence("bbbab") == 4

    def test_another_case(self):
        assert longest_palindrome_subsequence("cbbd") == 2

    def test_entire_string_palindrome(self):
        assert longest_palindrome_subsequence("racecar") == 7

    def test_single_character(self):
        assert longest_palindrome_subsequence("a") == 1

    def test_no_palindrome(self):
        assert longest_palindrome_subsequence("abc") == 1

    def test_empty_string(self):
        assert longest_palindrome_subsequence("") == 0


class TestDecodeWays:
    """Test decode_ways function."""

    def test_simple_case(self):
        assert decode_ways("12") == 2

    def test_complex_case(self):
        assert decode_ways("226") == 3

    def test_invalid_start(self):
        assert decode_ways("0") == 0

    def test_with_zero(self):
        assert decode_ways("10") == 1
        assert decode_ways("27") == 1

    def test_single_digit(self):
        assert decode_ways("1") == 1
        assert decode_ways("9") == 1

    def test_leading_zero_invalid(self):
        assert decode_ways("01") == 0

    def test_multiple_zeros(self):
        assert decode_ways("100") == 0

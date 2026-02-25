"""Test for most common word functionality."""

# 3rd party imports
import pytest

# Local imports
from src.aws_kuiper.most_common_word import most_common_word_v1, most_common_word_v2


class TestMostCommonWordV1:
    """Test most_common_word_v1 function."""

    def test_basic_case_with_banned_word(self):
        """Test basic case with banned words."""
        paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
        banned = ["hit"]
        result = most_common_word_v1(paragraph, banned)
        assert result == ("ball", 2)

    def test_punctuation_and_case_insensitive(self):
        """Test handling of punctuation and case insensitivity."""
        paragraph = "a, a, a, a, b,b,b,c, c"
        banned = ["a"]
        result = most_common_word_v1(paragraph, banned)
        assert result == ("b", 3)

    def test_single_word_no_banned(self):
        """Test single word with no banned words."""
        paragraph = "a."
        banned = []
        result = most_common_word_v1(paragraph, banned)
        assert result == ("a", 1)

    def test_multiple_words_same_frequency(self):
        """Test multiple words with same frequency returns first encountered."""
        paragraph = "apple banana apple banana cherry"
        banned = []
        result = most_common_word_v1(paragraph, banned)
        assert result[1] == 2  # frequency should be 2
        assert result[0] in ["apple", "banana"]  # either could be returned

    def test_all_words_banned_raises_error(self):
        """Test that ValueError is raised when all words are banned."""
        paragraph = "hello world"
        banned = ["hello", "world"]
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v1(paragraph, banned)

    def test_empty_paragraph_raises_error(self):
        """Test that ValueError is raised for empty paragraph."""
        paragraph = ""
        banned = []
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v1(paragraph, banned)

    def test_only_punctuation_raises_error(self):
        """Test that ValueError is raised for paragraph with only punctuation."""
        paragraph = "!@#$%^&*()"
        banned = []
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v1(paragraph, banned)

    def test_mixed_case_banned_words(self):
        """Test banned words with mixed case."""
        paragraph = "The QUICK brown fox jumps over the lazy dog"
        banned = ["The", "OVER"]
        result = most_common_word_v1(paragraph, banned)
        assert result[1] == 1  # all remaining words appear once

    def test_complex_punctuation(self):
        """Test complex punctuation handling."""
        paragraph = "It's a beautiful day! Isn't it? Yes, it is."
        banned = ["a", "is"]
        result = most_common_word_v1(paragraph, banned)
        assert result == ("it", 3)  # "it" appears 3 times

    def test_numbers_ignored(self):
        """Test that numbers are ignored."""
        paragraph = "There are 123 apples and 456 oranges"
        banned = []
        result = most_common_word_v1(paragraph, banned)
        assert result[1] == 1  # all words appear once, numbers ignored


class TestMostCommonWordV2:
    """Test most_common_word_v2 function."""

    def test_basic_case_with_banned_word(self):
        """Test basic case with banned words."""
        paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
        banned = ["hit"]
        result = most_common_word_v2(paragraph, banned)
        assert result == ("ball", 2)

    def test_punctuation_and_case_insensitive(self):
        """Test handling of punctuation and case insensitivity."""
        paragraph = "a, a, a, a, b,b,b,c, c"
        banned = ["a"]
        result = most_common_word_v2(paragraph, banned)
        assert result == ("b", 3)

    def test_single_word_no_banned(self):
        """Test single word with no banned words."""
        paragraph = "a."
        banned = []
        result = most_common_word_v2(paragraph, banned)
        assert result == ("a", 1)

    def test_multiple_words_same_frequency(self):
        """Test multiple words with same frequency returns first encountered."""
        paragraph = "apple banana apple banana cherry"
        banned = []
        result = most_common_word_v2(paragraph, banned)
        assert result[1] == 2  # frequency should be 2
        assert result[0] in ["apple", "banana"]  # either could be returned

    def test_all_words_banned_raises_error(self):
        """Test that ValueError is raised when all words are banned."""
        paragraph = "hello world"
        banned = ["hello", "world"]
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v2(paragraph, banned)

    def test_empty_paragraph_raises_error(self):
        """Test that ValueError is raised for empty paragraph."""
        paragraph = ""
        banned = []
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v2(paragraph, banned)

    def test_only_punctuation_raises_error(self):
        """Test that ValueError is raised for paragraph with only punctuation."""
        paragraph = "!@#$%^&*()"
        banned = []
        with pytest.raises(ValueError, match="No valid words found after filtering banned words"):
            most_common_word_v2(paragraph, banned)

    def test_mixed_case_banned_words(self):
        """Test banned words with mixed case."""
        paragraph = "The QUICK brown fox jumps over the lazy dog"
        banned = ["The", "OVER"]
        result = most_common_word_v2(paragraph, banned)
        assert result[1] == 1  # all remaining words appear once

    def test_complex_punctuation(self):
        """Test complex punctuation handling."""
        paragraph = "It's a beautiful day! Isn't it? Yes, it is."
        banned = ["a", "is"]
        result = most_common_word_v2(paragraph, banned)
        assert result == ("it", 3)  # "it" appears 3 times

    def test_numbers_ignored(self):
        """Test that numbers are ignored."""
        paragraph = "There are 123 apples and 456 oranges"
        banned = []
        result = most_common_word_v2(paragraph, banned)
        assert result[1] == 1  # all words appear once, numbers ignored

"""Tests for pattern matching and string searching algorithms."""

from src.string.pattern_matching import (
    find_substring_naive as find_needle_in_haystack,
    # Temporarily comment out missing functions until they're implemented
    # kmp_pattern_search,
    # rabin_karp_search,
    # z_algorithm_search,
    # wildcard_pattern_matching,
    # regular_expression_matching,
    # find_all_pattern_occurrences,
    # longest_prefix_suffix,
    # boyer_moore_search,
)


class TestFindNeedleInHaystack:
    """Test find_needle_in_haystack function."""

    def test_simple_match(self):
        assert find_needle_in_haystack("hello", "ll") == 2

    def test_no_match(self):
        assert find_needle_in_haystack("aaaaa", "bba") == -1

    def test_empty_needle(self):
        assert find_needle_in_haystack("hello", "") == 0

    def test_needle_longer_than_haystack(self):
        assert find_needle_in_haystack("abc", "abcde") == -1

    def test_exact_match(self):
        assert find_needle_in_haystack("hello", "hello") == 0

    def test_match_at_end(self):
        assert find_needle_in_haystack("hello", "lo") == 3

    def test_repeated_pattern(self):
        assert find_needle_in_haystack("aaaa", "aa") == 0


# TODO: Uncomment and implement these test classes when the corresponding functions are implemented

# class TestKMPPatternSearch:
#     """Test kmp_pattern_search function."""
#     pass

# class TestRabinKarpSearch:
#     """Test rabin_karp_search function."""
#     pass

# class TestZAlgorithmSearch:
#     """Test z_algorithm_search function."""
#     pass

# class TestWildcardPatternMatching:
#     """Test wildcard_pattern_matching function."""
#     pass

# class TestRegularExpressionMatching:
#     """Test regular_expression_matching function."""
#     pass

# class TestFindAllPatternOccurrences:
#     """Test find_all_pattern_occurrences function."""
#     pass

# class TestLongestPrefixSuffix:
#     """Test longest_prefix_suffix function."""
#     pass

# class TestBoyerMooreSearch:
#     """Test boyer_moore_search function."""
#     pass

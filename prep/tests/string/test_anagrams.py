"""Tests for anagram-related string operations."""

# from src.string.anagrams import (
#     are_anagram,
#     # group_anagrams,
#     # find_anagrams_in_string,
#     # anagram_mappings,
#     # valid_anagram_with_deletions,
#     # min_steps_to_anagram,
#     # check_anagram_frequency,
# )
from src.string.anagrams import (
    anagram_mappings,
    are_anagrams,
    are_anagrams_ignore_spaces,
    check_inclusion,
    group_anagrams,
    find_anagrams_in_string,
)


class TestAreAnagrams:
    """Test are_anagrams function."""

    def test_valid_anagrams(self):
        """Test valid anagrams."""
        assert are_anagrams("anagram", "nagaram")

    def test_invalid_anagrams(self):
        """Test invalid anagrams."""
        assert not are_anagrams("rat", "car")

    def test_empty_strings(self):
        """Test empty strings."""
        assert are_anagrams("", "")

    def test_single_character(self):
        """Test single character strings."""
        assert are_anagrams("a", "a")
        assert not are_anagrams("a", "b")

    def test_different_lengths(self):
        """Test strings of different lengths."""
        assert not are_anagrams("abc", "abcd")

    def test_case_sensitive(self):
        """Test case sensitivity."""
        assert not are_anagrams("Listen", "Silent")
        assert are_anagrams("listen", "silent")

    def test_with_spaces(self):
        """Test strings with spaces."""
        assert not are_anagrams("a b", "ba")
        assert are_anagrams("a b", "b a")


class TestAreAnagramsIgnoreSpaces:
    """Test are_anagrams_ignore_spaces function."""

    def test_valid_anagrams_with_spaces(self):
        """Test valid anagrams with spaces and case differences."""
        assert are_anagrams_ignore_spaces("The Eyes", "They See")
        assert are_anagrams_ignore_spaces("A gentleman", "Elegant man")
        assert are_anagrams_ignore_spaces("Conversation", "Voices rant on")

    def test_invalid_anagrams_with_spaces(self):
        """Test invalid anagrams with spaces."""
        assert not are_anagrams_ignore_spaces("hello", "world")
        assert not are_anagrams_ignore_spaces("not an", "anagram")

    def test_case_insensitive(self):
        """Test case insensitive comparison."""
        assert are_anagrams_ignore_spaces("Listen", "Silent")
        assert are_anagrams_ignore_spaces("EVIL", "vile")
        assert are_anagrams_ignore_spaces("Astronomer", "Moon starer")

    def test_multiple_spaces(self):
        """Test strings with multiple spaces."""
        assert are_anagrams_ignore_spaces("a  b  c", "c b a")
        assert are_anagrams_ignore_spaces("  listen  ", "  silent  ")

    def test_empty_and_spaces_only(self):
        """Test empty strings and space-only strings."""
        assert are_anagrams_ignore_spaces("", "")
        assert are_anagrams_ignore_spaces("   ", "")
        assert are_anagrams_ignore_spaces("", "   ")

    def test_single_character_with_spaces(self):
        """Test single character with spaces."""
        assert are_anagrams_ignore_spaces(" a ", "a")
        assert are_anagrams_ignore_spaces("A", " a ")

    def test_different_lengths_after_normalization(self):
        """Test strings that have different lengths after removing spaces."""
        assert not are_anagrams_ignore_spaces("a b c", "ab")
        assert not are_anagrams_ignore_spaces("hello world", "helloworld!")


class TestGroupAnagrams:
    """Test group_anagrams function."""

    def test_simple_grouping(self):
        """Test simple grouping of anagrams."""
        strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        result = group_anagrams(strs)

        # Convert to sets for easier comparison
        result_sets = [set(group) for group in result]
        expected_sets = [{"eat", "tea", "ate"}, {"tan", "nat"}, {"bat"}]

        assert len(result_sets) == len(expected_sets)
        for expected_set in expected_sets:
            assert expected_set in result_sets

    def test_empty_list(self):
        """Test empty list input."""
        assert group_anagrams([]) == []

    def test_single_string(self):
        """Test list with a single string."""
        result = group_anagrams(["abc"])
        assert result == [["abc"]]

    def test_all_same_anagrams(self):
        """Test all strings are anagrams."""
        strs = ["abc", "bca", "cab"]
        result = group_anagrams(strs)
        assert len(result) == 1
        assert set(result[0]) == {"abc", "bca", "cab"}

    def test_no_anagrams(self):
        """Test list with no anagrams."""
        strs = ["abc", "def", "ghi"]
        result = group_anagrams(strs)
        assert len(result) == 3
        for group in result:
            assert len(group) == 1


class TestFindAnagramsInString:
    """Test find_anagrams_in_string function."""

    def test_simple_case(self):
        """Test simple case with overlapping anagrams."""
        result = find_anagrams_in_string("abab", "ab")
        assert sorted(result) == [0, 1, 2]  # "ab", "ba", "ab" are all anagrams

    def test_no_anagrams(self):
        """Test case with no anagrams present."""
        result = find_anagrams_in_string("abcd", "ef")
        assert result == []

    def test_overlapping_anagrams(self):
        """Test case with overlapping anagrams."""
        result = find_anagrams_in_string("abcab", "abc")
        assert sorted(result) == [0, 1, 2]  # "abc", "bca", "cab" are all anagrams

    def test_pattern_longer_than_string(self):
        """Test case where pattern is longer than string."""
        result = find_anagrams_in_string("abc", "abcd")
        assert result == []

    def test_same_length(self):
        """Test case where string and pattern are of same length."""
        result = find_anagrams_in_string("abc", "bca")
        assert result == [0]

    def test_repeated_characters(self):
        """Test case with repeated characters in string and pattern."""
        result = find_anagrams_in_string("aaab", "aab")
        assert result == [1]  # Only "aab" at position 1 is an anagram of "aab"


class TestAnagramMappings:
    """Test anagram_mappings function."""

    def test_simple_mapping(self):
        """Test simple anagram mapping."""
        result = anagram_mappings([12, 28, 46, 32, 50], [50, 12, 32, 46, 28])
        assert result == [1, 4, 3, 2, 0]

    def test_identity_mapping(self):
        """Test identity mapping."""
        result = anagram_mappings([1, 2, 3], [1, 2, 3])
        assert result == [0, 1, 2]

    def test_reverse_mapping(self):
        """Test reverse mapping."""
        result = anagram_mappings([1, 2, 3], [3, 2, 1])
        assert result == [2, 1, 0]

    def test_single_element(self):
        """Test single element mapping."""
        result = anagram_mappings([42], [42])
        assert result == [0]

    def test_with_duplicates(self):
        """Test mapping with duplicates."""
        result = anagram_mappings([1, 1, 2], [2, 1, 1])
        # Should map to any valid permutation
        assert len(result) == 3
        assert sorted(result) == [0, 1, 2]


class TestCheckInclusion:
    """Test check_inclusion function."""

    def test_basic_inclusion_true(self):
        """Test basic case where permutation exists."""
        assert check_inclusion("ab", "eidbaooo")
        assert check_inclusion("ab", "eidbaoo")

    def test_basic_inclusion_false(self):
        """Test basic case where permutation doesn't exist."""
        assert not check_inclusion("ab", "eidboaoo")

    def test_exact_match(self):
        """Test when s1 exactly matches a substring in s2."""
        assert check_inclusion("abc", "abcdef")
        assert check_inclusion("abc", "defabc")
        assert check_inclusion("abc", "defabcghi")

    def test_permutation_match(self):
        """Test when a permutation of s1 exists in s2."""
        assert check_inclusion("abc", "bac")
        assert check_inclusion("abc", "defbacghi")
        assert check_inclusion("abc", "defcabghi")

    def test_no_match(self):
        """Test when no permutation exists."""
        assert not check_inclusion("abc", "def")
        assert not check_inclusion("abc", "ab")  # Missing 'c'
        assert check_inclusion("abc", "abcd")  # Has all letters

    def test_repeated_characters(self):
        """Test with repeated characters."""
        assert check_inclusion("aab", "abab")
        assert check_inclusion("aab", "baa")
        assert not check_inclusion("aab", "ab")  # Missing one 'a'
        assert check_inclusion("aa", "aaa")

    def test_single_character(self):
        """Test single character cases."""
        assert check_inclusion("a", "abc")
        assert not check_inclusion("a", "bcd")
        assert check_inclusion("a", "a")

    def test_empty_strings(self):
        """Test edge cases with empty strings."""
        assert check_inclusion("", "abc")
        assert not check_inclusion("a", "")

    def test_same_length_strings(self):
        """Test when both strings have same length."""
        assert check_inclusion("abc", "bca")
        assert not check_inclusion("abc", "def")
        assert check_inclusion("abc", "abc")

    def test_pattern_longer_than_text(self):
        """Test when pattern is longer than text."""
        assert not check_inclusion("abcd", "abc")
        assert not check_inclusion("abc", "ab")

    def test_case_sensitive(self):
        """Test case sensitivity."""
        assert check_inclusion("Ab", "bA")
        assert not check_inclusion("Ab", "ba")
        assert not check_inclusion("ab", "AB")


# class TestValidAnagramWithDeletions:
#     """Test valid_anagram_with_deletions function."""

#     def test_valid_with_deletions(self):
#         assert valid_anagram_with_deletions("anagram", "grammar") == True

#     def test_exact_anagrams(self):
#         assert valid_anagram_with_deletions("listen", "silent") == True

#     def test_impossible_anagram(self):
#         assert valid_anagram_with_deletions("abc", "def") == False

#     def test_empty_strings(self):
#         assert valid_anagram_with_deletions("", "") == True

#     def test_one_empty_string(self):
#         assert valid_anagram_with_deletions("abc", "") == True
#         assert valid_anagram_with_deletions("", "abc") == True

#     def test_subset_letters(self):
#         assert valid_anagram_with_deletions("abcdef", "abc") == True
#         assert valid_anagram_with_deletions("abc", "abcdef") == False


# class TestMinStepsToAnagram:
#     """Test min_steps_to_anagram function."""

#     def test_simple_case(self):
#         assert min_steps_to_anagram("bab", "aba") == 1

#     def test_no_steps_needed(self):
#         assert min_steps_to_anagram("anagram", "nagaram") == 0

#     def test_different_lengths(self):
#         # Should return -1 or handle appropriately
#         result = min_steps_to_anagram("abc", "abcd")
#         assert result == -1 or result > 0

#     def test_completely_different(self):
#         assert min_steps_to_anagram("abc", "def") == 3

#     def test_single_character(self):
#         assert min_steps_to_anagram("a", "a") == 0
#         assert min_steps_to_anagram("a", "b") == 1

#     def test_empty_strings(self):
#         assert min_steps_to_anagram("", "") == 0


# class TestCheckAnagramFrequency:
#     """Test check_anagram_frequency function."""

#     def test_matching_frequencies(self):
#         freq1 = {'a': 2, 'b': 1, 'c': 1}
#         freq2 = {'c': 1, 'a': 2, 'b': 1}
#         assert check_anagram_frequency(freq1, freq2) == True

#     def test_different_frequencies(self):
#         freq1 = {'a': 2, 'b': 1}
#         freq2 = {'a': 1, 'b': 2}
#         assert check_anagram_frequency(freq1, freq2) == False

#     def test_different_keys(self):
#         freq1 = {'a': 1, 'b': 1}
#         freq2 = {'c': 1, 'd': 1}
#         assert check_anagram_frequency(freq1, freq2) == False

#     def test_empty_frequencies(self):
#         assert check_anagram_frequency({}, {}) == True

#     def test_one_empty_frequency(self):
#         freq1 = {'a': 1}
#         freq2 = {}
#         assert check_anagram_frequency(freq1, freq2) == False

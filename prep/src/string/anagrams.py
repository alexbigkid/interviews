"""Anagram algorithms for interview preparation."""


def are_anagrams(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s1: First string
        s2: Second string

    Returns:
        True if strings are anagrams

    Examples:
        >>> are_anagrams("listen", "silent")
        True
        >>> are_anagrams("evil", "vile")
        True
        >>> are_anagrams("hello", "world")
        False
    """
    if len(s1) != len(s2):
        return False
    return sorted(s1) == sorted(s2)


def are_anagrams_ignore_spaces(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams ignoring spaces and case.

    Time: O(n), Space: O(k)

    Args:
        s1: First string
        s2: Second string

    Returns:
        True if strings are anagrams

    Examples:
        >>> are_anagrams_ignore_spaces("The Eyes", "They See")
        True
        >>> are_anagrams_ignore_spaces("A gentleman", "Elegant man")
        True
        >>> are_anagrams_ignore_spaces("hello", "world")
        False
    """
    norm_s1 = s1.replace(" ", "").lower()
    norm_s2 = s2.replace(" ", "").lower()
    if len(norm_s1) != len(norm_s2):
        return False
    return sorted(norm_s1) == sorted(norm_s2)


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group strings that are anagrams of each other.

    Time: O(n*k*log(k)) where n is number of strings, k is max length
    Space: O(n*k)

    Args:
        strs: List of strings

    Returns:
        List of groups where each group contains anagrams

    Examples:
        >>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
        >>> group_anagrams([""])
        [['']]
    """
    if len(strs) == 0:
        return []

    anagram_map = {}
    for s in strs:
        key = "".join(sorted(s))
        anagram_map.setdefault(key, []).append(s)
    return list(anagram_map.values())


def find_anagrams_in_string(s: str, p: str) -> list[int]:
    """Find all start indices of anagrams of p in s.

    Time: O(n), Space: O(k) where k is unique characters in p

    Args:
        s: String to search in
        p: Pattern to find anagrams of

    Returns:
        List of starting indices where anagrams of p occur

    Examples:
        >>> find_anagrams_in_string("abab", "ab")
        [0, 2]
        >>> find_anagrams_in_string("abacabad", "aab")
        [1, 4]
        >>> find_anagrams_in_string("abc", "xyz")
        []
    """
    if len(p) > len(s):
        return []

    # Count characters in pattern
    p_count = {}
    for char in p:
        p_count[char] = p_count.get(char, 0) + 1

    # Initialize window with first len(p) characters
    window_count = {}
    for _i, char in enumerate(s[: len(p)]):
        window_count[char] = window_count.get(char, 0) + 1

    result = []

    # Check first window
    if window_count == p_count:
        result.append(0)

    # Slide the window
    for i, new_char in enumerate(s[len(p) :], len(p)):
        # Add new character (right side of window)
        window_count[new_char] = window_count.get(new_char, 0) + 1

        # Remove old character (left side of window)
        old_char = s[i - len(p)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]

        # Check if current window is an anagram
        if window_count == p_count:
            result.append(i - len(p) + 1)

    return result


def min_window_anagram(s: str, t: str) -> str:
    """Find minimum window in s that contains all characters of t.

    Time: O(n), Space: O(k) where k is unique characters in t

    Args:
        s: Source string
        t: Target string containing required characters

    Returns:
        Minimum window substring or empty string if not found

    Examples:
        >>> min_window_anagram("ADOBECODEBANC", "ABC")
        'BANC'
        >>> min_window_anagram("a", "a")
        'a'
        >>> min_window_anagram("a", "aa")
        ''
    """
    # TODO: Implement this function
    raise NotImplementedError


def anagram_mappings(a: list[int], b: list[int]) -> list[int]:
    """Find anagram mapping between two arrays.

    Time: O(n), Space: O(n)

    Args:
        a: First array
        b: Second array (anagram of first)

    Returns:
        Array mapping indices from a to b

    Examples:
        >>> anagram_mappings([12, 28, 46, 32, 50], [50, 12, 32, 46, 28])
        [1, 4, 3, 2, 0]
    """
    index_map = {}
    for i, num in enumerate(b):
        if num in index_map:
            index_map[num].append(i)
        else:
            index_map[num] = [i]

    result = []
    for num in a:
        result.append(index_map[num].pop())
    return result


def check_inclusion(s1: str, s2: str) -> bool:
    """Check if any permutation of s1 is a substring of s2.

    Time: O(n), Space: O(k) where k is unique characters in s1

    Args:
        s1: Pattern string
        s2: Text string

    Returns:
        True if any permutation of s1 is substring of s2

    Examples:
        >>> check_inclusion("ab", "eidbaooo")
        True
        >>> check_inclusion("ab", "eidboaoo")
        False
    """
    s1_count = {}
    for char in s1:
        s1_count[char] = s1_count.get(char, 0) + 1

    window_count = {}
    left = 0
    for _i, char in enumerate(s2):
        window_count[char] = window_count.get(char, 0) + 1
        while window_count.get(char, 0) > s1_count.get(char, 0):
            window_count[s2[left]] -= 1
            if window_count[s2[left]] == 0:
                del window_count[s2[left]]
            left += 1

        if window_count == s1_count:
            return True

    return False


def longest_anagram_substring(s: str) -> int:
    """Find length of longest substring with at most 2 distinct characters that can form an anagram.

    Time: O(n), Space: O(1)

    Args:
        s: Input string

    Returns:
        Length of longest valid substring

    Examples:
        >>> longest_anagram_substring("abacbc")
        4
        >>> longest_anagram_substring("aabbcc")
        6
    """
    # TODO: Implement this function
    raise NotImplementedError


def anagram_difference(s1: str, s2: str) -> int:
    """Find minimum number of character deletions to make strings anagrams.

    Time: O(n), Space: O(k)

    Args:
        s1: First string
        s2: Second string

    Returns:
        Minimum deletions needed

    Examples:
        >>> anagram_difference("cde", "abc")
        4
        >>> anagram_difference("listen", "silent")
        0
    """
    # TODO: Implement this function
    raise NotImplementedError


def count_anagram_substrings(s: str) -> int:
    """Count number of substrings that are anagrams of any other substring.

    Time: O(n³), Space: O(n²)

    Args:
        s: Input string

    Returns:
        Number of anagram substring pairs

    Examples:
        >>> count_anagram_substrings("abba")
        4
        >>> count_anagram_substrings("abab")
        2
    """
    # TODO: Implement this function
    raise NotImplementedError

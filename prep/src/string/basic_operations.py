"""Basic string operations for interview preparation."""

import logging

from src.shared.performance_timer import PerformanceTimer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reverse_string(s: str) -> str:
    """Reverse a string.

    Time: O(n), Space: O(n)

    Args:
        s: Input string

    Returns:
        Reversed string

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("a")
        'a'
        >>> reverse_string("")
        ''
    """
    # with PerformanceTimer("reverse_string1", logger):
    #     reverse_1 = s[::-1]
    # with PerformanceTimer("reverse_string2", logger):
    #     reverse_1 = ''.join(reversed(s))
    with PerformanceTimer("reverse_string3", logger):
        reverse_1 = ""
        for char in s:
            reverse_1 = char + reverse_1
    return reverse_1


def reverse_string_inplace(s: list[str]) -> None:
    """Reverse a string in-place (modify the input list).

    Time: O(n), Space: O(1)

    Args:
        s: List of characters to reverse in-place

    Examples:
        >>> chars = ["h", "e", "l", "l", "o"]
        >>> reverse_string_inplace(chars)
        >>> chars
        ['o', 'l', 'l', 'e', 'h']
    """
    # with PerformanceTimer("reverse_string_array1", logger):
    #     for i in range(len(s) // 2):
    #         s[i], s[len(s) - 1 - i] = s[len(s) - 1 - i], s[i]
    with PerformanceTimer("reverse_string_array2", logger):
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1


def rotate_string_left(s: str, k: int) -> str:
    """Rotate string left by k positions.

    Time: O(n), Space: O(n)

    Args:
        s: Input string
        k: Number of positions to rotate left

    Returns:
        Rotated string

    Examples:
        >>> rotate_string_left("abcdef", 2)
        'cdefab'
        >>> rotate_string_left("hello", 1)
        'elloh'
        >>> rotate_string_left("abc", 3)
        'abc'
    """
    if len(s) == 0 or k <= 0:
        return s
    k = k % len(s)  # Handle cases where k >= n
    return s[k:] + s[:k]


def character_frequency(s: str) -> dict[str, int]:
    """Count frequency of each character in string.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Input string

    Returns:
        Dictionary mapping characters to their frequencies

    Examples:
        >>> character_frequency("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
        >>> character_frequency("aabbcc")
        {'a': 2, 'b': 2, 'c': 2}
        >>> character_frequency("")
        {}
    """
    char_freq = {}
    # with PerformanceTimer("character_frequency", logger):
    #     for char in s:
    #         if char in char_freq:
    #             char_freq[char] += 1
    #         else:
    #             char_freq[char] = 1
    with PerformanceTimer("character_frequency", logger):
        for char in s:
            char_freq[char] = char_freq.get(char, 0) + 1
    return char_freq


def most_frequent_character(s: str) -> str:
    """Find the most frequently occurring character.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Input string

    Returns:
        Most frequent character (first one if tie)

    Examples:
        >>> most_frequent_character("hello")
        'l'
        >>> most_frequent_character("aabbcc")
        'a'

    Raises:
        ValueError: If string is empty
    """
    if len(s) == 0:
        raise ValueError("Input string is empty")

    most_freq_char = ""
    max_count = 0
    with PerformanceTimer("most_frequent_character", logger):
        for char in s:
            count = s.count(char)
            if count > max_count:
                max_count = count
                most_freq_char = char
    return most_freq_char
    # with PerformanceTimer("most_frequent_character", logger):
    #     char_freq = character_frequency(s)
    # return max(char_freq, key=char_freq.get)


def remove_duplicates(s: str) -> str:
    """Remove duplicate characters while preserving order.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Input string

    Returns:
        String with duplicates removed

    Examples:
        >>> remove_duplicates("hello")
        'helo'
        >>> remove_duplicates("aabbcc")
        'abc'
        >>> remove_duplicates("")
        ''
    """
    with PerformanceTimer("remove_duplicates", logger):
        # seen = []
        # for char in s:
        #     if char not in seen:
        #         seen.append(char)
        # ret_val = ''.join(seen)
        seen = set()
        ret_val = "".join([char for char in s if not (char in seen or seen.add(char))])
    return ret_val


def is_subsequence(s: str, t: str) -> bool:
    """Check if s is a subsequence of t.

    Time: O(n), Space: O(1) where n is length of t

    Args:
        s: Potential subsequence
        t: Target string

    Returns:
        True if s is subsequence of t

    Examples:
        >>> is_subsequence("ace", "abcde")
        True
        >>> is_subsequence("aec", "abcde")
        False
        >>> is_subsequence("", "abc")
        True
    """
    # if len(s) == 0:
    #     return True
    # if len(t) == 0 or len(s) > len(t):
    #     return False

    # si, ti = 0, 0
    # while si < len(s) and ti < len(t):
    #     if s[si] == t[ti]:
    #         si += 1
    #     ti += 1
    # return si == len(s)
    iter_t = iter(t)
    return all(char in iter_t for char in s)


def first_unique_character(s: str) -> int:
    """Find index of first non-repeating character.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Input string

    Returns:
        Index of first unique character, -1 if none exists

    Examples:
        >>> first_unique_character("leetcode")
        0
        >>> first_unique_character("loveleetcode")
        2
        >>> first_unique_character("aabb")
        -1
    """
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    for i, char in enumerate(s):
        if char_count[char] == 1:
            return i
    return -1


def main():
    """Main function for manual testing."""
    # test_str = "Hello World!"
    # print(f"Reversed string: {reverse_string(test_str)}")

    # test_str = ["h", "e", "l", "l", "o", "", "w", "o", "r", "l", "d"]
    # reverse_string_inplace(test_str)
    # print(f"Reversed string array: {test_str}")

    # test_str = "123456789"
    # print(test_str)
    # print(rotate_string_left(test_str, 3))

    # char_freq = character_frequency("hello world!")
    # print(json.dumps(char_freq, indent=4))

    # char = most_frequent_character("hello world!")
    # print(f"Most frequent character: {char}")

    no_dups = remove_duplicates("programming, hello, world, hello Kuiper Project")
    print(f"String without duplicates: {no_dups}")


if __name__ == "__main__":
    main()

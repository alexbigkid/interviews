"""Palindrome algorithms for interview preparation."""


def is_palindrome(s: str) -> bool:
    """Check if string is a palindrome (simple version).

    Time: O(n), Space: O(1)

    Args:
        s: Input string

    Returns:
        True if string is palindrome

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("")
        True
    """
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
    # return s == s[::-1]


def is_palindrome_ignore_case_punctuation(s: str) -> bool:
    """Check if string is palindrome ignoring case and non-alphanumeric chars.

    Time: O(n), Space: O(1)

    Args:
        s: Input string

    Returns:
        True if string is palindrome

    Examples:
        >>> is_palindrome_ignore_case_punctuation("A man, a plan, a canal: Panama")
        True
        >>> is_palindrome_ignore_case_punctuation("race a car")
        False
        >>> is_palindrome_ignore_case_punctuation("")
        True
    """
    norm_s = "".join(c.lower() for c in s if c.isalnum())
    return norm_s == norm_s[::-1]


def longest_palindrome_substring(s: str) -> str:
    """Find longest palindromic substring using expand around centers.

    Time: O(n²), Space: O(1)

    Args:
        s: Input string

    Returns:
        Longest palindromic substring

    Examples:
        >>> longest_palindrome_substring("babad")
        'bab'
        >>> longest_palindrome_substring("cbbd")
        'bb'
        >>> longest_palindrome_substring("a")
        'a'
    """
    # Option 1
    # def expand(l: int, r: int) -> tuple[int, int]:
    #     while l >= 0 and r < len(s) and s[l] == s[r]:
    #         l -= 1
    #         r += 1
    #     return l + 1, r - 1  # inclusive bounds of palindrome

    # start = end = 0
    # for i in range(len(s)):
    #     for l, r in (expand(i, i), expand(i, i + 1)):  # odd + even
    #         if r - l > end - start:
    #             start, end = l, r

    # return s[start:end + 1]

    # Option 2
    if len(s) == 0:
        return ""

    start, end = 0, 0

    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(len(s)):
        len1 = expand_around_center(i, i)  # Odd length
        len2 = expand_around_center(i, i + 1)  # Even length
        max_len = max(len1, len2)
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2

    return s[start : end + 1]


def palindromic_substrings_count(s: str) -> int:
    """Count all palindromic substrings in the string.

    Time: O(n²), Space: O(1)

    Args:
        s: Input string

    Returns:
        Number of palindromic substrings

    Examples:
        >>> palindromic_substrings_count("abc")
        3
        >>> palindromic_substrings_count("aaa")
        6
        >>> palindromic_substrings_count("aba")
        4
    """
    count = 0

    def expand_around_center(left: int, right: int) -> int:
        local_count = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            local_count += 1
            left -= 1
            right += 1
        return local_count

    for i in range(len(s)):
        count += expand_around_center(i, i)  # Odd length
        count += expand_around_center(i, i + 1)  # Even length

    return count


def shortest_palindrome(s: str) -> str:
    """Find shortest palindrome by adding characters to front.

    Time: O(n²), Space: O(n)

    Args:
        s: Input string

    Returns:
        Shortest palindrome by prepending characters

    Examples:
        >>> shortest_palindrome("aacecaaa")
        'aaacecaaa'
        >>> shortest_palindrome("abcd")
        'dcbabcd'
    """
    if not s:
        return s

    def is_palindrome_check(subs: str) -> bool:
        return subs == subs[::-1]

    for i in range(len(s), -1, -1):
        if is_palindrome_check(s[:i]):
            to_add = s[i:][::-1]
            return to_add + s

    return s  # Fallback, should not reach here


def valid_palindrome_ii(s: str) -> bool:
    """Check if string can be palindrome after deleting at most one character.

    Time: O(n), Space: O(1)

    Args:
        s: Input string

    Returns:
        True if can form palindrome by removing at most one character

    Examples:
        >>> valid_palindrome_ii("aba")
        True
        >>> valid_palindrome_ii("abca")
        True
        >>> valid_palindrome_ii("abc")
        False
    """

    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome_range(left + 1, right) or is_palindrome_range(left, right - 1)
        left += 1
        right -= 1
    return True


def palindrome_pairs(words: list[str]) -> list[tuple[int, int]]:
    """Find all pairs of words that form palindromes when concatenated.

    Time: O(n²*m) where n is number of words, m is average length
    Space: O(n*m)

    Args:
        words: List of words

    Returns:
        List of index pairs that form palindromes

    Examples:
        >>> palindrome_pairs(["race", "car"])
        [(1, 0)]
        >>> palindrome_pairs(["lls", "s", "sssll"])
        [(0, 1), (2, 0)]
    """

    def is_palindrome_check(s: str) -> bool:
        return s == s[::-1]

    result = []
    n = len(words)

    for i in range(n):
        for j in range(n):
            if i != j:
                combined = words[i] + words[j]
                if is_palindrome_check(combined):
                    result.append((i, j))

    return result


def can_form_palindrome(s: str) -> bool:
    """Check if characters in string can be rearranged to form palindrome.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Input string

    Returns:
        True if characters can form palindrome

    Examples:
        >>> can_form_palindrome("carerac")
        True
        >>> can_form_palindrome("code")
        False
        >>> can_form_palindrome("aab")
        True
    """
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1

    odd_count = sum(1 for count in char_count.values() if count % 2 != 0)
    return odd_count <= 1


def longest_palindrome_by_removing_chars(s: str) -> int:
    """Find length of longest palindrome by removing characters.

    Time: O(n²), Space: O(n²)

    Args:
        s: Input string

    Returns:
        Length of longest possible palindrome

    Examples:
        >>> longest_palindrome_by_removing_chars("bbbab")
        4
        >>> longest_palindrome_by_removing_chars("cbbd")
        2
    """
    n = len(s)
    if n == 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):  # length of substring
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + (dp[i + 1][j - 1] if length > 2 else 0)
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]

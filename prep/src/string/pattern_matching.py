"""Pattern matching algorithms for interview preparation."""


def find_substring_naive(text: str, pattern: str) -> int:
    """Find first occurrence of pattern in text using naive approach.

    Time: O(n*m), Space: O(1)

    Args:
        text: Text to search in
        pattern: Pattern to find

    Returns:
        Index of first occurrence, -1 if not found

    Examples:
        >>> find_substring_naive("hello world", "world")
        6
        >>> find_substring_naive("abcdef", "xyz")
        -1
        >>> find_substring_naive("", "a")
        -1
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    for i in range(n - m + 1):
        if text[i : i + m] == pattern:
            return i
    return -1


def build_kmp_table(pattern: str) -> list[int]:
    """Build KMP failure function table.

    Time: O(m), Space: O(m) where m is pattern length

    Args:
        pattern: Pattern to build table for

    Returns:
        KMP failure function table

    Examples:
        >>> build_kmp_table("ABABCABAB")
        [0, 0, 1, 2, 0, 1, 2, 3, 4]
        >>> build_kmp_table("AAAA")
        [0, 1, 2, 3]
    """
    m = len(pattern)
    if m == 0:
        return []

    lps = [0] * m  # Longest proper prefix which is also suffix
    length = 0  # Length of previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def find_substring_kmp(text: str, pattern: str) -> int:
    """Find first occurrence of pattern using KMP algorithm.

    Time: O(n+m), Space: O(m)

    Args:
        text: Text to search in
        pattern: Pattern to find

    Returns:
        Index of first occurrence, -1 if not found

    Examples:
        >>> find_substring_kmp("hello world", "world")
        6
        >>> find_substring_kmp("ABABDABACDABABCABAB", "ABABCABAB")
        10
    """
    if not pattern:
        return 0
    if not text:
        return -1

    n, m = len(text), len(pattern)
    if m > n:
        return -1

    # Build KMP table
    lps = build_kmp_table(pattern)

    i = j = 0  # Indices for text and pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            return i - j  # Found at index i - j
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def find_all_occurrences(text: str, pattern: str) -> list[int]:
    """Find all occurrences of pattern in text.

    Time: O(n+m), Space: O(k+m) where k is number of matches

    Args:
        text: Text to search in
        pattern: Pattern to find

    Returns:
        List of indices where pattern occurs

    Examples:
        >>> find_all_occurrences("abababab", "ab")
        [0, 2, 4, 6]
        >>> find_all_occurrences("hello", "ll")
        [2]
        >>> find_all_occurrences("abc", "xyz")
        []
    """
    if not pattern:
        return []
    if not text:
        return []

    n, m = len(text), len(pattern)
    if m > n:
        return []

    # Build KMP table
    lps = build_kmp_table(pattern)

    result = []
    i = j = 0  # Indices for text and pattern

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)  # Found at index i - j
            j = lps[j - 1]  # Continue searching for more occurrences
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result


def wildcard_match(text: str, pattern: str) -> bool:
    """Match text against pattern with wildcards (? and *).

    ? matches single character, * matches any sequence.

    Time: O(n*m), Space: O(n*m)

    Args:
        text: Text to match
        pattern: Pattern with wildcards

    Returns:
        True if text matches pattern

    Examples:
        >>> wildcard_match("adceb", "*a*b*")
        True
        >>> wildcard_match("acdcb", "a*c?b")
        False
        >>> wildcard_match("abc", "a?c")
        True
    """
    n, m = len(text), len(pattern)

    # DP table: dp[i][j] = True if text[0:i] matches pattern[0:j]
    dp = [[False] * (m + 1) for _ in range(n + 1)]

    # Empty pattern matches empty text
    dp[0][0] = True

    # Handle patterns starting with *
    for j in range(1, m + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if pattern[j - 1] == "*":
                # * can match empty sequence or any character
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif pattern[j - 1] == "?" or pattern[j - 1] == text[i - 1]:
                # ? matches any single character, or exact match
                dp[i][j] = dp[i - 1][j - 1]

    return dp[n][m]


def regex_match(text: str, pattern: str) -> bool:
    """Match text against regex pattern with . and *. matches single character, * matches zero or more of preceding.

    Time: O(n*m), Space: O(n*m)

    Args:
        text: Text to match
        pattern: Regex pattern

    Returns:
        True if text matches pattern

    Examples:
        >>> regex_match("aa", "a")
        False
        >>> regex_match("aa", "a*")
        True
        >>> regex_match("ab", ".*")
        True
    """
    n, m = len(text), len(pattern)

    # DP table: dp[i][j] = True if text[0:i] matches pattern[0:j]
    dp = [[False] * (m + 1) for _ in range(n + 1)]

    # Empty pattern matches empty text
    dp[0][0] = True

    # Handle patterns like a*, a*b*, a*b*c* (can match empty string)
    for j in range(2, m + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]

    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if pattern[j - 1] == "*":
                # * can match zero or more of preceding character
                dp[i][j] = dp[i][j - 2]  # Match zero occurrences

                # Match one or more occurrences if preceding char matches
                if pattern[j - 2] == "." or pattern[j - 2] == text[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif pattern[j - 1] == "." or pattern[j - 1] == text[i - 1]:
                # . matches any character, or exact match
                dp[i][j] = dp[i - 1][j - 1]

    return dp[n][m]


def longest_common_prefix(strs: list[str]) -> str:
    """Find longest common prefix among array of strings.

    Time: O(S) where S is sum of all characters, Space: O(1)

    Args:
        strs: List of strings

    Returns:
        Longest common prefix

    Examples:
        >>> longest_common_prefix(["flower", "flow", "flight"])
        'fl'
        >>> longest_common_prefix(["dog", "racecar", "car"])
        ''
        >>> longest_common_prefix([""])
        ''
    """
    if not strs:
        return ""

    if len(strs) == 1:
        return strs[0]

    # Find minimum length string
    min_len = min(len(s) for s in strs)

    for i in range(min_len):
        char = strs[0][i]
        for s in strs[1:]:
            if s[i] != char:
                return strs[0][:i]

    return strs[0][:min_len]


def string_to_integer(s: str) -> int:
    """Convert string to integer (atoi implementation).

    Handle whitespace, signs, and overflow.

    Time: O(n), Space: O(1)

    Args:
        s: String to convert

    Returns:
        Integer value, clamped to 32-bit signed integer range

    Examples:
        >>> string_to_integer("42")
        42
        >>> string_to_integer("   -42")
        -42
        >>> string_to_integer("4193 with words")
        4193
        >>> string_to_integer("words and 987")
        0
    """
    if not s:
        return 0

    # Constants for 32-bit signed integer range
    INT_MAX = 2**31 - 1
    INT_MIN = -(2**31)

    i = 0
    n = len(s)

    # Skip leading whitespace
    while i < n and s[i] == " ":
        i += 1

    if i >= n:
        return 0

    # Check for sign
    sign = 1
    if s[i] == "-":
        sign = -1
        i += 1
    elif s[i] == "+":
        i += 1

    # Convert digits
    result = 0
    while i < n and s[i].isdigit():
        digit = int(s[i])

        # Check for overflow before multiplying
        if result > (INT_MAX - digit) // 10:
            return INT_MAX if sign == 1 else INT_MIN

        result = result * 10 + digit
        i += 1

    return sign * result


def count_and_say(n: int) -> str:
    """Generate the nth term of count-and-say sequence.

    Time: O(4^n), Space: O(4^n)

    Args:
        n: Term number (1-indexed)

    Returns:
        nth term of sequence

    Examples:
        >>> count_and_say(1)
        '1'
        >>> count_and_say(4)
        '1211'
        >>> count_and_say(5)
        '111221'
    """
    if n <= 0:
        return ""

    current = "1"

    for _ in range(1, n):
        next_term = ""
        i = 0

        while i < len(current):
            count = 1
            char = current[i]

            # Count consecutive identical characters
            while i + count < len(current) and current[i + count] == char:
                count += 1

            # Append count and character to next term
            next_term += str(count) + char
            i += count

        current = next_term

    return current

"""Advanced string algorithms for interview preparation."""


def edit_distance(word1: str, word2: str) -> int:
    """Find minimum edit distance (Levenshtein distance) between two strings.

    Time: O(m*n), Space: O(m*n)

    Args:
        word1: First string
        word2: Second string

    Returns:
        Minimum number of operations (insert, delete, replace) needed

    Examples:
        >>> edit_distance("horse", "ros")
        3
        >>> edit_distance("intention", "execution")
        5
        >>> edit_distance("", "abc")
        3
    """
    m, n = len(word1), len(word2)

    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to get word2

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # Delete
                    dp[i][j - 1],  # Insert
                    dp[i - 1][j - 1],  # Replace
                )

    return dp[m][n]


def edit_distance_space_optimized(word1: str, word2: str) -> int:
    """Find edit distance with O(min(m,n)) space complexity.

    Time: O(m*n), Space: O(min(m,n))

    Args:
        word1: First string
        word2: Second string

    Returns:
        Minimum edit distance

    Examples:
        >>> edit_distance_space_optimized("horse", "ros")
        3
        >>> edit_distance_space_optimized("intention", "execution")
        5
    """
    m, n = len(word1), len(word2)

    # Make sure word2 is the shorter string for space optimization
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m

    # Use two arrays instead of full DP table
    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev

    return prev[n]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """Find length of longest common subsequence.

    Time: O(m*n), Space: O(m*n)

    Args:
        text1: First string
        text2: Second string

    Returns:
        Length of longest common subsequence

    Examples:
        >>> longest_common_subsequence("abcde", "ace")
        3
        >>> longest_common_subsequence("abc", "abc")
        3
        >>> longest_common_subsequence("abc", "def")
        0
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def longest_common_substring(text1: str, text2: str) -> int:
    """Find length of longest common substring.

    Time: O(m*n), Space: O(m*n)

    Args:
        text1: First string
        text2: Second string

    Returns:
        Length of longest common substring

    Examples:
        >>> longest_common_substring("abcdxyz", "xyzabcd")
        4
        >>> longest_common_substring("zxabcdezy", "yzabcdezx")
        6
    """
    if not text1 or not text2:
        return 0

    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_length = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_length = max(max_length, dp[i][j])
            else:
                dp[i][j] = 0  # Reset for substring

    return max_length


def is_interleaving(s1: str, s2: str, s3: str) -> bool:
    """Check if s3 is formed by interleaving s1 and s2.

    Time: O(m*n), Space: O(m*n)

    Args:
        s1: First string
        s2: Second string
        s3: Target interleaved string

    Returns:
        True if s3 is interleaving of s1 and s2

    Examples:
        >>> is_interleaving("aabcc", "dbbca", "aadbbcbcac")
        True
        >>> is_interleaving("aabcc", "dbbca", "aadbbbaccc")
        False
    """
    m, n, k = len(s1), len(s2), len(s3)

    # Length check
    if m + n != k:
        return False

    # DP table: dp[i][j] = True if s3[0:i+j] can be formed by interleaving s1[0:i] and s2[0:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Fill first column (using only s1)
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]

    # Fill first row (using only s2)
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]

    # Fill the rest of the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])

    return dp[m][n]


def distinct_subsequences(s: str, t: str) -> int:
    """Count distinct subsequences of s that equal t.

    Time: O(m*n), Space: O(m*n)

    Args:
        s: Source string
        t: Target subsequence

    Returns:
        Number of distinct subsequences

    Examples:
        >>> distinct_subsequences("rabbbit", "rabbit")
        3
        >>> distinct_subsequences("babgbag", "bag")
        5
    """
    m, n = len(s), len(t)

    # dp[i][j] = number of ways to form t[0:j] using s[0:i]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Empty string t can be formed in one way (by taking nothing)
    for i in range(m + 1):
        dp[i][0] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Don't use current character from s
            dp[i][j] = dp[i - 1][j]

            # If characters match, add ways using current character
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]

    return dp[m][n]


def word_break(s: str, wordDict: list[str]) -> bool:
    """Check if string can be segmented into dictionary words.

    Time: O(n²), Space: O(n)

    Args:
        s: Input string
        wordDict: Dictionary of valid words

    Returns:
        True if string can be segmented

    Examples:
        >>> word_break("leetcode", ["leet", "code"])
        True
        >>> word_break("applepenapple", ["apple", "pen"])
        True
        >>> word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
        False
    """
    if not s:
        return True

    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty string can be segmented

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    """Find all possible ways to break string into dictionary words.

    Time: O(2^n), Space: O(2^n)

    Args:
        s: Input string
        wordDict: Dictionary of valid words

    Returns:
        List of all possible sentence breakdowns

    Examples:
        >>> word_break_ii("catsanddog", ["cat", "cats", "and", "sand", "dog"])
        ['cats and dog', 'cat sand dog']
    """
    word_set = set(wordDict)
    memo = {}

    def backtrack(s):
        if s in memo:
            return memo[s]

        if not s:
            return [""]

        result = []
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in word_set:
                if i == len(s):  # Last word
                    result.append(word)
                else:
                    rest_sentences = backtrack(s[i:])
                    for sentence in rest_sentences:
                        result.append(word + " " + sentence)

        memo[s] = result
        return result

    return backtrack(s)


def scramble_string(s1: str, s2: str) -> bool:
    """Check if s2 is a scrambled version of s1.

    Time: O(n⁴), Space: O(n³)

    Args:
        s1: Original string
        s2: Potentially scrambled string

    Returns:
        True if s2 is scramble of s1

    Examples:
        >>> scramble_string("great", "rgeat")
        True
        >>> scramble_string("abcdef", "fecabd")
        True
        >>> scramble_string("abcd", "acbd")
        False
    """
    if len(s1) != len(s2):
        return False

    if s1 == s2:
        return True

    # Character frequency check
    if sorted(s1) != sorted(s2):
        return False

    memo = {}

    def helper(s1, s2):
        if (s1, s2) in memo:
            return memo[(s1, s2)]

        if len(s1) != len(s2):
            return False

        if s1 == s2:
            return True

        if sorted(s1) != sorted(s2):
            return False

        for i in range(1, len(s1)):
            # Case 1: No swap at position i
            if helper(s1[:i], s2[:i]) and helper(s1[i:], s2[i:]):
                memo[(s1, s2)] = True
                return True

            # Case 2: Swap at position i
            if helper(s1[:i], s2[len(s2) - i :]) and helper(s1[i:], s2[: len(s2) - i]):
                memo[(s1, s2)] = True
                return True

        memo[(s1, s2)] = False
        return False

    return helper(s1, s2)


def minimum_window_with_chars(s: str, chars: str) -> str:
    """Find minimum window containing all required characters.

    Time: O(n), Space: O(k) where k is unique characters

    Args:
        s: Source string
        chars: Required characters

    Returns:
        Minimum window or empty string if impossible

    Examples:
        >>> minimum_window_with_chars("ADOBECODEBANC", "ABC")
        'BANC'
        >>> minimum_window_with_chars("a", "a")
        'a'
    """
    if not s or not chars:
        return ""

    from collections import Counter

    # Count characters needed
    chars_count = Counter(chars)
    required = len(chars_count)

    # Sliding window
    left = right = 0
    formed = 0
    window_counts = {}

    # Answer: (window length, left, right)
    ans = float("inf"), None, None

    while right < len(s):
        # Expand window by including character at right
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        # Check if current character contributes to required count
        if char in chars_count and window_counts[char] == chars_count[char]:
            formed += 1

        # Try to contract window until it ceases to be 'desirable'
        while left <= right and formed == required:
            char = s[left]

            # Save smallest window
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)

            # Remove leftmost character from window
            window_counts[char] -= 1
            if char in chars_count and window_counts[char] < chars_count[char]:
                formed -= 1

            left += 1

        right += 1

    return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]


def longest_palindrome_subsequence(s: str) -> int:
    """Find length of longest palindromic subsequence.

    Time: O(n²), Space: O(n²)

    Args:
        s: Input string

    Returns:
        Length of longest palindromic subsequence

    Examples:
        >>> longest_palindrome_subsequence("bbbab")
        4
        >>> longest_palindrome_subsequence("cbbd")
        2
    """
    n = len(s)
    if n == 0:
        return 0

    # dp[i][j] = length of longest palindromic subsequence in s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Single characters are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1

    # Fill for substrings of length 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


def decode_ways(s: str) -> int:
    """Count number of ways to decode a numeric string to letters.

    '1' -> 'A', '2' -> 'B', ..., '26' -> 'Z'.

    Time: O(n), Space: O(n)

    Args:
        s: Numeric string to decode

    Returns:
        Number of ways to decode

    Examples:
        >>> decode_ways("12")
        2
        >>> decode_ways("226")
        3
        >>> decode_ways("0")
        0
    """
    if not s or s[0] == "0":
        return 0

    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty string has 1 way
    dp[1] = 1  # First character (if not '0')

    for i in range(2, n + 1):
        # Single digit decode
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]

        # Two digit decode
        two_digit = int(s[i - 2 : i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]

    return dp[n]

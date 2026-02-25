"""Dynamic programming problems using arrays for interview preparation."""


def coin_change(coins: list[int], amount: int) -> int:
    """Find minimum number of coins needed to make amount.

    Time: O(amount * len(coins)), Space: O(amount)

    Args:
        coins: Available coin denominations
        amount: Target amount

    Returns:
        Minimum coins needed, -1 if impossible

    Examples:
        >>> coin_change([1, 3, 4], 6)
        2
        >>> coin_change([2], 3)
        -1
        >>> coin_change([1], 0)
        0
    """
    if amount == 0:
        return 0

    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


def coin_change_combinations(coins: list[int], amount: int) -> int:
    """Count number of ways to make amount using coins.

    Time: O(amount * len(coins)), Space: O(amount)

    Args:
        coins: Available coin denominations
        amount: Target amount

    Returns:
        Number of combinations

    Examples:
        >>> coin_change_combinations([1, 2, 5], 5)
        4
        >>> coin_change_combinations([2], 3)
        0
        >>> coin_change_combinations([10], 10)
        1
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make amount 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]


def longest_increasing_subsequence(nums: list[int]) -> int:
    """Find length of longest increasing subsequence.

    Time: O(n log n), Space: O(n)

    Args:
        nums: Input array

    Returns:
        Length of LIS

    Examples:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
        >>> longest_increasing_subsequence([0, 1, 0, 3, 2, 3])
        4
        >>> longest_increasing_subsequence([7, 7, 7, 7, 7, 7, 7])
        1
    """
    if not nums:
        return 0

    import bisect

    # dp[i] stores the smallest ending element of LIS of length i+1
    dp = []

    for num in nums:
        pos = bisect.bisect_left(dp, num)
        if pos == len(dp):
            dp.append(num)
        else:
            dp[pos] = num

    return len(dp)


def longest_increasing_subsequence_sequence(nums: list[int]) -> list[int]:
    """Find actual longest increasing subsequence.

    Time: O(n log n), Space: O(n)

    Args:
        nums: Input array

    Returns:
        One possible LIS

    Examples:
        >>> longest_increasing_subsequence_sequence([10, 9, 2, 5, 3, 7, 101, 18])
        [2, 3, 7, 18]
    """
    if not nums:
        return []

    import bisect

    n = len(nums)
    dp = []  # stores smallest ending element of LIS of length i+1
    parent = [-1] * n  # to reconstruct sequence
    dp_indices = []  # indices in dp array

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(dp, num)

        if pos == len(dp):
            dp.append(num)
            dp_indices.append(i)
        else:
            dp[pos] = num
            dp_indices[pos] = i

        # Set parent for reconstruction
        if pos > 0:
            parent[i] = dp_indices[pos - 1]

    # Reconstruct LIS
    result = []
    if dp:
        idx = dp_indices[-1]
        while idx != -1:
            result.append(nums[idx])
            idx = parent[idx]

    result.reverse()
    return result


def maximum_product_subarray(nums: list[int]) -> int:
    """Find maximum product of contiguous subarray.

    Time: O(n), Space: O(1)

    Args:
        nums: Array of integers

    Returns:
        Maximum product

    Examples:
        >>> maximum_product_subarray([2, 3, -2, 4])
        6
        >>> maximum_product_subarray([-2, 0, -1])
        0
        >>> maximum_product_subarray([-2, 3, -4])
        24
    """
    if not nums:
        return 0

    max_prod = nums[0]
    min_prod = nums[0]
    result = nums[0]

    for i in range(1, len(nums)):
        num = nums[i]

        # When we multiply by negative number, max becomes min and min becomes max
        if num < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)

        result = max(result, max_prod)

    return result


def house_robber(nums: list[int]) -> int:
    """Maximum money that can be robbed without robbing adjacent houses.

    Time: O(n), Space: O(1)

    Args:
        nums: Money in each house

    Returns:
        Maximum money that can be robbed

    Examples:
        >>> house_robber([1, 2, 3, 1])
        4
        >>> house_robber([2, 7, 9, 3, 1])
        12
        >>> house_robber([5])
        5
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = nums[0]
    prev1 = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current

    return prev1


def house_robber_circular(nums: list[int]) -> int:
    """House robber with houses arranged in a circle.

    Time: O(n), Space: O(1)

    Args:
        nums: Money in each house (arranged in circle)

    Returns:
        Maximum money that can be robbed

    Examples:
        >>> house_robber_circular([2, 3, 2])
        3
        >>> house_robber_circular([1, 2, 3, 1])
        4
        >>> house_robber_circular([1, 2, 3])
        3
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    def rob_linear(arr):
        if not arr:
            return 0
        if len(arr) == 1:
            return arr[0]

        prev2 = arr[0]
        prev1 = max(arr[0], arr[1])

        for i in range(2, len(arr)):
            current = max(prev1, prev2 + arr[i])
            prev2 = prev1
            prev1 = current

        return prev1

    # Case 1: Rob houses 0 to n-2 (exclude last)
    # Case 2: Rob houses 1 to n-1 (exclude first)
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def jump_game(nums: list[int]) -> bool:
    """Check if you can reach the last index.

    Time: O(n), Space: O(1)

    Args:
        nums: Array where nums[i] is max jump length from position i

    Returns:
        True if last index is reachable

    Examples:
        >>> jump_game([2, 3, 1, 1, 4])
        True
        >>> jump_game([3, 2, 1, 0, 4])
        False
        >>> jump_game([0])
        True
    """
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False

        max_reach = max(max_reach, i + nums[i])

        if max_reach >= len(nums) - 1:
            return True

    return True


def jump_game_min_jumps(nums: list[int]) -> int:
    """Find minimum number of jumps to reach last index.

    Time: O(n), Space: O(1)

    Args:
        nums: Array where nums[i] is max jump length from position i

    Returns:
        Minimum jumps needed

    Examples:
        >>> jump_game_min_jumps([2, 3, 1, 1, 4])
        2
        >>> jump_game_min_jumps([2, 3, 0, 1, 4])
        2
        >>> jump_game_min_jumps([1, 1, 1, 1])
        3
    """
    if len(nums) <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps


def unique_paths_grid(m: int, n: int) -> int:
    """Number of unique paths in m x n grid from top-left to bottom-right.

    Time: O(m * n), Space: O(n)

    Args:
        m: Number of rows
        n: Number of columns

    Returns:
        Number of unique paths

    Examples:
        >>> unique_paths_grid(3, 7)
        28
        >>> unique_paths_grid(3, 2)
        3
        >>> unique_paths_grid(1, 1)
        1
    """
    # Use space-optimized DP
    dp = [1] * n

    for _i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]

    return dp[n - 1]


def unique_paths_with_obstacles(obstacleGrid: list[list[int]]) -> int:
    """Number of unique paths with obstacles.

    Time: O(m * n), Space: O(n)

    Args:
        obstacleGrid: Grid where 1 represents obstacle, 0 is free

    Returns:
        Number of unique paths

    Examples:
        >>> unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        2
        >>> unique_paths_with_obstacles([[0, 1], [0, 0]])
        1
    """
    if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
        return 0

    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [0] * n
    dp[0] = 1

    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]

    return dp[n - 1]


def minimum_path_sum(grid: list[list[int]]) -> int:
    """Find path from top-left to bottom-right with minimum sum.

    Time: O(m * n), Space: O(n)

    Args:
        grid: Grid of non-negative integers

    Returns:
        Minimum path sum

    Examples:
        >>> minimum_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
        7
        >>> minimum_path_sum([[1, 2, 3], [4, 5, 6]])
        12
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [float("inf")] * n
    dp[0] = grid[0][0]

    # Initialize first row
    for j in range(1, n):
        dp[j] = dp[j - 1] + grid[0][j]

    for i in range(1, m):
        dp[0] += grid[i][0]  # First column
        for j in range(1, n):
            dp[j] = min(dp[j], dp[j - 1]) + grid[i][j]

    return dp[n - 1]


def climbing_stairs(n: int) -> int:
    """Number of ways to climb n stairs (1 or 2 steps at a time).

    Time: O(n), Space: O(1)

    Args:
        n: Number of stairs

    Returns:
        Number of ways to climb

    Examples:
        >>> climbing_stairs(2)
        2
        >>> climbing_stairs(3)
        3
        >>> climbing_stairs(4)
        5
    """
    if n <= 0:
        return 1 if n == 0 else 0
    if n <= 2:
        return n

    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2

    for _i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


def decode_ways_dp(s: str) -> int:
    """Number of ways to decode numeric string to letters.

    Time: O(n), Space: O(1)

    Args:
        s: String of digits

    Returns:
        Number of ways to decode

    Examples:
        >>> decode_ways_dp("12")
        2
        >>> decode_ways_dp("226")
        3
        >>> decode_ways_dp("0")
        0
    """
    if not s or s[0] == "0":
        return 0

    n = len(s)
    if n == 1:
        return 1

    prev2 = 1  # dp[i-2]
    prev1 = 1  # dp[i-1]

    for i in range(1, n):
        current = 0

        # Single digit
        if s[i] != "0":
            current += prev1

        # Two digits
        two_digit = int(s[i - 1 : i + 1])
        if 10 <= two_digit <= 26:
            current += prev2

        prev2 = prev1
        prev1 = current

    return prev1


def word_break_dp(s: str, wordDict: list[str]) -> bool:
    """Check if string can be segmented using dictionary words.

    Time: O(n² + m*k), Space: O(n + m*k)
    where n=len(s), m=len(wordDict), k=avg word length

    Args:
        s: String to segment
        wordDict: Dictionary of valid words

    Returns:
        True if segmentation possible

    Examples:
        >>> word_break_dp("leetcode", ["leet", "code"])
        True
        >>> word_break_dp("applepenapple", ["apple", "pen"])
        True
        >>> word_break_dp("catsandog", ["cats", "dog", "sand", "and", "cat"])
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


def partition_equal_subset_sum(nums: list[int]) -> bool:
    """Check if array can be partitioned into two equal sum subsets.

    Time: O(n * sum), Space: O(sum)

    Args:
        nums: Array of positive integers

    Returns:
        True if equal partition exists

    Examples:
        >>> partition_equal_subset_sum([1, 5, 11, 5])
        True
        >>> partition_equal_subset_sum([1, 2, 3, 5])
        False
        >>> partition_equal_subset_sum([1, 2, 5])
        False
    """
    total_sum = sum(nums)

    # If total sum is odd, cannot partition equally
    if total_sum % 2 != 0:
        return False

    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True  # Sum 0 is always possible (empty subset)

    for num in nums:
        # Traverse backwards to avoid using same element multiple times
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]

    return dp[target]

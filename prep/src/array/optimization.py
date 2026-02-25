"""Array optimization techniques and space/time complexity improvements."""


def sort_colors(nums: list[int]) -> None:
    """Sort array of 0s, 1s, and 2s in-place (Dutch flag problem).

    Time: O(n), Space: O(1)

    Args:
        nums: Array containing only 0s, 1s, and 2s

    Examples:
        >>> nums = [2, 0, 2, 1, 1, 0]
        >>> sort_colors(nums)
        >>> nums
        [0, 0, 1, 1, 2, 2]
    """
    # Three-way partitioning
    left = 0  # Next position for 0
    right = len(nums) - 1  # Next position for 2
    current = 0

    while current <= right:
        if nums[current] == 0:
            nums[left], nums[current] = nums[current], nums[left]
            left += 1
            current += 1
        elif nums[current] == 2:
            nums[current], nums[right] = nums[right], nums[current]
            right -= 1
            # Don't increment current as we need to check swapped element
        else:  # nums[current] == 1
            current += 1


def merge_sorted_arrays_inplace(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """Merge two sorted arrays in-place.

    Time: O(m + n), Space: O(1)

    Args:
        nums1: First sorted array with space for second array
        m: Number of elements in nums1
        nums2: Second sorted array
        n: Number of elements in nums2

    Examples:
        >>> nums1 = [1, 2, 3, 0, 0, 0]
        >>> merge_sorted_arrays_inplace(nums1, 3, [2, 5, 6], 3)
        >>> nums1
        [1, 2, 2, 3, 5, 6]
    """
    # Start from the end to avoid overwriting
    i = m - 1  # Last element in nums1
    j = n - 1  # Last element in nums2
    k = m + n - 1  # Last position in merged array

    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1


def remove_duplicates_sorted_ii(nums: list[int]) -> int:
    """Remove duplicates allowing at most 2 duplicates in-place.

    Time: O(n), Space: O(1)

    Args:
        nums: Sorted array to modify

    Returns:
        New length after removing excess duplicates

    Examples:
        >>> nums = [1, 1, 1, 2, 2, 3]
        >>> remove_duplicates_sorted_ii(nums)
        5
        >>> nums[:5]
        [1, 1, 2, 2, 3]
    """
    if len(nums) <= 2:
        return len(nums)

    write_index = 2

    for read_index in range(2, len(nums)):
        if nums[read_index] != nums[write_index - 2]:
            nums[write_index] = nums[read_index]
            write_index += 1

    return write_index


def find_duplicate_number(nums: list[int]) -> int:
    """Find duplicate number using Floyd's algorithm (constant space).

    Time: O(n), Space: O(1)

    Args:
        nums: Array of n+1 integers where each integer is 1 ≤ nums[i] ≤ n

    Returns:
        The duplicate number

    Examples:
        >>> find_duplicate_number([1, 3, 4, 2, 2])
        2
        >>> find_duplicate_number([3, 1, 3, 4, 2])
        3
    """
    if not nums:
        return -1

    # For invalid input, fall back to simple approach
    n = len(nums) - 1
    for num in nums:
        if num < 1 or num > n:
            # Use simple counting approach
            from collections import Counter

            counter = Counter(nums)
            for num, count in counter.items():
                if count > 1:
                    return num
            return -1

    # Floyd's cycle detection algorithm for valid input
    slow = fast = nums[0]

    # Phase 1: Find intersection point in the cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find start of cycle (duplicate number)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


def missing_number_xor(nums: list[int]) -> int:
    """Find missing number using XOR (constant space).

    Time: O(n), Space: O(1)

    Args:
        nums: Array containing n distinct numbers in range [0, n]

    Returns:
        The missing number

    Examples:
        >>> missing_number_xor([3, 0, 1])
        2
        >>> missing_number_xor([0, 1])
        2
        >>> missing_number_xor([9, 6, 4, 2, 3, 5, 7, 0, 1])
        8
    """
    n = len(nums)
    missing = n

    for i in range(n):
        missing ^= i ^ nums[i]

    return missing


def single_number_xor(nums: list[int]) -> int:
    """Find single number where every other number appears twice.

    Time: O(n), Space: O(1)

    Args:
        nums: Array where every element appears twice except one

    Returns:
        The single number

    Examples:
        >>> single_number_xor([2, 2, 1])
        1
        >>> single_number_xor([4, 1, 2, 1, 2])
        4
        >>> single_number_xor([1])
        1
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def single_number_ii(nums: list[int]) -> int:
    """Find single number where every other number appears three times.

    Time: O(n), Space: O(1)

    Args:
        nums: Array where every element appears three times except one

    Returns:
        The single number

    Examples:
        >>> single_number_ii([2, 2, 3, 2])
        3
        >>> single_number_ii([0, 1, 0, 1, 0, 1, 99])
        99
    """
    ones = twos = 0

    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones


def majority_element_boyer_moore(nums: list[int]) -> int:
    """Find majority element using Boyer-Moore algorithm.

    Time: O(n), Space: O(1)

    Args:
        nums: Array where majority element appears more than n/2 times

    Returns:
        The majority element

    Examples:
        >>> majority_element_boyer_moore([3, 2, 3])
        3
        >>> majority_element_boyer_moore([2, 2, 1, 1, 1, 2, 2])
        2
    """
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1

    return candidate


def wiggle_sort(nums: list[int]) -> None:
    """Wiggle sort in-place: nums[0] < nums[1] > nums[2] < nums[3]...

    Time: O(n), Space: O(1)

    Args:
        nums: Array to sort in wiggle pattern

    Examples:
        >>> nums = [3, 5, 2, 1, 6, 4]
        >>> wiggle_sort(nums)
        >>> # nums should satisfy wiggle pattern
    """
    for i in range(len(nums) - 1):
        if (i % 2 == 0 and nums[i] > nums[i + 1]) or (i % 2 == 1 and nums[i] < nums[i + 1]):
            nums[i], nums[i + 1] = nums[i + 1], nums[i]


def next_permutation(nums: list[int]) -> None:
    """Find next lexicographically greater permutation in-place.

    Time: O(n), Space: O(1)

    Args:
        nums: Array to find next permutation of

    Examples:
        >>> nums = [1, 2, 3]
        >>> next_permutation(nums)
        >>> nums
        [1, 3, 2]
    """
    i = len(nums) - 2

    # Find rightmost character smaller than its next character
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Find ceiling of nums[i] in nums[i+1:]
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # Reverse the suffix
    nums[i + 1 :] = reversed(nums[i + 1 :])


def longest_consecutive_sequence(nums: list[int]) -> int:
    """Find longest consecutive sequence length.

    Time: O(n), Space: O(n)

    Args:
        nums: Unsorted array of integers

    Returns:
        Length of longest consecutive sequence

    Examples:
        >>> longest_consecutive_sequence([100, 4, 200, 1, 3, 2])
        4
        >>> longest_consecutive_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])
        9
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start counting if this is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length


def kth_largest_element(nums: list[int], k: int) -> int:
    """Find kth largest element using quickselect.

    Time: O(n) average, O(n²) worst, Space: O(1)

    Args:
        nums: Array of integers
        k: Position of largest element to find

    Returns:
        Kth largest element

    Examples:
        >>> kth_largest_element([3, 2, 1, 5, 6, 4], 2)
        5
        >>> kth_largest_element([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
        4
    """
    import random

    def partition(left, right, pivot_idx):
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        store_idx = left

        for i in range(left, right):
            if nums[i] > pivot:  # For kth largest, we want larger elements first
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1

        nums[right], nums[store_idx] = nums[store_idx], nums[right]
        return store_idx

    def quickselect(left, right, k_smallest):
        if left == right:
            return nums[left]

        pivot_idx = random.randint(left, right)  # noqa: S311
        pivot_idx = partition(left, right, pivot_idx)

        if k_smallest == pivot_idx:
            return nums[k_smallest]
        elif k_smallest < pivot_idx:
            return quickselect(left, pivot_idx - 1, k_smallest)
        else:
            return quickselect(pivot_idx + 1, right, k_smallest)

    return quickselect(0, len(nums) - 1, k - 1)


def top_k_frequent_elements(nums: list[int], k: int) -> list[int]:
    """Find k most frequent elements using bucket sort.

    Time: O(n), Space: O(n)

    Args:
        nums: Array of integers
        k: Number of most frequent elements to return

    Returns:
        K most frequent elements

    Examples:
        >>> top_k_frequent_elements([1, 1, 1, 2, 2, 3], 2)
        [1, 2]
        >>> top_k_frequent_elements([1], 1)
        [1]
    """
    from collections import Counter

    # Count frequencies
    count = Counter(nums)

    # Create bucket array where index is frequency
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]

    # Place elements in buckets by frequency
    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect k most frequent elements from highest frequency buckets
    result = []
    for i in range(n, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            break

    return result[:k]


def range_sum_query_immutable(nums: list[int]):
    """Design data structure for range sum queries.

    Init: O(n), Query: O(1), Space: O(n)

    Args:
        nums: Array for preprocessing

    Returns:
        NumArray object with sumRange method

    Examples:
        >>> num_array = range_sum_query_immutable([-2, 0, 3, -5, 2, -1])
        >>> num_array.sumRange(0, 2)  # sum of [-2, 0, 3]
        1
        >>> num_array.sumRange(2, 5)  # sum of [3, -5, 2, -1]
        -1
    """

    class NumArray:
        def __init__(self, nums: list[int]):
            self.prefix_sums = [0]
            for num in nums:
                self.prefix_sums.append(self.prefix_sums[-1] + num)

        def sumRange(self, left: int, right: int) -> int:
            return self.prefix_sums[right + 1] - self.prefix_sums[left]

    return NumArray(nums)


def range_sum_query_2d_immutable(matrix: list[list[int]]):
    """Design data structure for 2D range sum queries.

    Init: O(m * n), Query: O(1), Space: O(m * n)

    Args:
        matrix: 2D matrix for preprocessing

    Returns:
        NumMatrix object with sumRegion method

    Examples:
        >>> num_matrix = range_sum_query_2d_immutable(
        ...     [[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]
        ... )
        >>> num_matrix.sumRegion(2, 1, 4, 3)
        8
    """

    class NumMatrix:
        def __init__(self, matrix: list[list[int]]):
            if not matrix or not matrix[0]:
                self.prefix_sums = []
                return

            m, n = len(matrix), len(matrix[0])
            self.prefix_sums = [[0] * (n + 1) for _ in range(m + 1)]

            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    self.prefix_sums[i][j] = (
                        matrix[i - 1][j - 1]
                        + self.prefix_sums[i - 1][j]
                        + self.prefix_sums[i][j - 1]
                        - self.prefix_sums[i - 1][j - 1]
                    )

        def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
            return (
                self.prefix_sums[row2 + 1][col2 + 1]
                - self.prefix_sums[row1][col2 + 1]
                - self.prefix_sums[row2 + 1][col1]
                + self.prefix_sums[row1][col1]
            )

    return NumMatrix(matrix)


def sparse_matrix_multiplication(mat1: list[list[int]], mat2: list[list[int]]) -> list[list[int]]:
    """Multiply two sparse matrices efficiently.

    Time: O(m * k * n) where non-zeros dominate, Space: O(m * n)

    Args:
        mat1: First sparse matrix
        mat2: Second sparse matrix

    Returns:
        Result of matrix multiplication

    Examples:
        >>> sparse_matrix_multiplication([[1, 0, 0], [-1, 0, 3]], [[7, 0, 0], [0, 0, 0], [0, 0, 1]])
        [[7, 0, 0], [-7, 0, 3]]
    """
    if not mat1 or not mat1[0] or not mat2 or not mat2[0]:
        return []

    m, k, n = len(mat1), len(mat1[0]), len(mat2[0])
    result = [[0] * n for _ in range(m)]

    # Precompute non-zero elements in mat2 for efficiency
    mat2_non_zero = {}
    for j in range(k):
        for col in range(n):
            if mat2[j][col] != 0:
                if j not in mat2_non_zero:
                    mat2_non_zero[j] = []
                mat2_non_zero[j].append((col, mat2[j][col]))

    for i in range(m):
        for j in range(k):
            if mat1[i][j] != 0 and j in mat2_non_zero:
                for col, val in mat2_non_zero[j]:
                    result[i][col] += mat1[i][j] * val

    return result

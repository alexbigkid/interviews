"""Basic array operations and fundamental algorithms for interview preparation."""


# Removed unused import to avoid shadowing


def two_sum(nums: list[int], target: int) -> list[int]:
    """Find two numbers that add up to target.

    Time: O(n), Space: O(n)

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        Indices of the two numbers that add up to target

    Examples:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
        >>> two_sum([3, 2, 4], 6)
        [1, 2]
        >>> two_sum([3, 3], 6)
        [0, 1]
    """
    # for i, n in enumerate(nums):
    #     if (second_num := target - n) in nums[i + 1:]:
    #         return [i, nums.index(second_num, i + 1)]
    # return []
    seen = {}
    for i, num in enumerate(nums):
        if (complement := target - num) in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def three_sum(nums: list[int]) -> list[list[int]]:
    """Find all unique triplets that sum to zero.

    Time: O(n²), Space: O(1) excluding output

    Args:
        nums: List of integers

    Returns:
        List of unique triplets that sum to zero

    Examples:
        >>> three_sum([-1, 0, 1, 2, -1, -4])
        [[-1, -1, 2], [-1, 0, 1]]
        >>> three_sum([0, 1, 1])
        []
        >>> three_sum([0, 0, 0])
        [[0, 0, 0]]
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # Skip duplicate first elements

        left, right = i + 1, n - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum < 0:
                left += 1
            elif current_sum > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1  # Skip duplicate second elements
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1  # Skip duplicate third elements
                left += 1
                right -= 1

    return result


def container_with_most_water(height: list[int]) -> int:
    """Find the maximum area that can be formed by two lines.

    Time: O(n), Space: O(1)

    Args:
        height: Array of non-negative integers representing heights

    Returns:
        Maximum area of water that can be contained

    Examples:
        >>> container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
        49
        >>> container_with_most_water([1, 1])
        1
        >>> container_with_most_water([4, 3, 2, 1, 4])
        16
    """
    left, right = 0, len(height) - 1
    max_area = 0

    while left < right:
        width = right - left
        current_area = min(height[left], height[right]) * width
        max_area = max(max_area, current_area)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_area


def remove_duplicates_sorted(nums: list[int]) -> int:
    """Remove duplicates from sorted array in-place.

    Time: O(n), Space: O(1)

    Args:
        nums: Sorted array to modify in-place

    Returns:
        New length of array after removing duplicates

    Examples:
        >>> nums = [1, 1, 2]
        >>> remove_duplicates_sorted(nums)
        2
        >>> nums[:2]
        [1, 2]
    """
    if len(nums) <= 1:
        return len(nums)

    write_index = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            nums[write_index] = nums[i]
            write_index += 1

    return write_index


def remove_element(nums: list[int], val: int) -> int:
    """Remove all instances of val in-place.

    Time: O(n), Space: O(1)

    Args:
        nums: Array to modify
        val: Value to remove

    Returns:
        New length after removal

    Examples:
        >>> nums = [3, 2, 2, 3]
        >>> remove_element(nums, 3)
        2
        >>> sorted(nums[:2])
        [2, 2]
    """
    if len(nums) == 0:
        return 0

    write_index = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[write_index] = nums[i]
            write_index += 1
    return write_index


def move_zeros(nums: list[int]) -> None:
    """Move all zeros to end while maintaining relative order.

    Time: O(n), Space: O(1)

    Args:
        nums: Array to modify in-place

    Examples:
        >>> nums = [0, 1, 0, 3, 12]
        >>> move_zeros(nums)
        >>> nums
        [1, 3, 12, 0, 0]
    """
    if len(nums) == 0:
        return

    write_index = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[write_index] = nums[i]
            write_index += 1

    for i in range(write_index, len(nums)):
        nums[i] = 0
    # nums[write_index:] = [0] * (len(nums) - write_index)  # One liner!


def find_pivot_index(nums: list[int]) -> int:
    """Find pivot index where left sum equals right sum.

    Time: O(n), Space: O(1)

    Args:
        nums: Array of integers

    Returns:
        Leftmost pivot index, -1 if none exists

    Examples:
        >>> find_pivot_index([1, 7, 3, 6, 5, 6])
        3
        >>> find_pivot_index([1, 2, 3])
        -1
        >>> find_pivot_index([2, 1, -1])
        0
    """
    total_sum = sum(nums)
    left_sum = 0

    for i, num in enumerate(nums):
        if left_sum == (total_sum - left_sum - num):
            return i
        left_sum += num

    return -1


def running_sum(nums: list[int]) -> list[int]:
    """Calculate running sum of array.

    Time: O(n), Space: O(1) excluding output

    Args:
        nums: Input array

    Returns:
        Array where result[i] = sum(nums[0]...nums[i])

    Examples:
        >>> running_sum([1, 2, 3, 4])
        [1, 3, 6, 10]
        >>> running_sum([1, 1, 1, 1, 1])
        [1, 2, 3, 4, 5]
        >>> running_sum([3, 1, 2, 10, 1])
        [3, 4, 6, 16, 17]
    """
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]
    return nums


def max_subarray_sum(nums: list[int]) -> int:
    """Find maximum sum of contiguous subarray (Kadane's algorithm).

    Time: O(n), Space: O(1)

    Args:
        nums: Array of integers

    Returns:
        Maximum sum of contiguous subarray

    Examples:
        >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        6
        >>> max_subarray_sum([1])
        1
        >>> max_subarray_sum([5, 4, -1, 7, 8])
        23
    """
    max_current = max_global = nums[0]
    for i in range(1, len(nums)):
        max_current = max(nums[i], max_current + nums[i])
        max_global = max(max_global, max_current)
    return max_global


def buy_sell_stock(prices: list[int]) -> int:
    """Find maximum profit from single buy/sell transaction.

    Time: O(n), Space: O(1)

    Args:
        prices: Array of stock prices

    Returns:
        Maximum profit possible

    Examples:
        >>> buy_sell_stock([7, 1, 5, 3, 6, 4])
        5
        >>> buy_sell_stock([7, 6, 4, 3, 1])
        0
        >>> buy_sell_stock([1, 2, 3, 4, 5])
        4
    """
    # min_price = float('inf')
    # max_profit = 0
    # for price in prices:
    #     if price < min_price:
    #         min_price = price
    #     elif price - min_price > max_profit:
    #         max_profit = price - min_price
    # return max_profit

    if len(prices) < 2:
        return 0
    min_price = prices[0]
    max_profit = 0
    for price in prices[1:]:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit

    # this is NOT working because the max price might come before min price
    # if len(prices) < 2:
    #     return 0
    # min_price = max_price = (0, prices[0])  # (index, price)
    # for i, price in enumerate(prices):
    #     if price < min_price[1]:
    #         min_price = (i, price)
    #     elif price > max_price[1]:
    #         max_price = (i, price)
    # if max_price[0] < min_price[0]:
    #     return 0
    # return max_price[1] - min_price[1]


def product_except_self(nums: list[int]) -> list[int]:
    """Return array where output[i] = product of all elements except nums[i].

    Time: O(n), Space: O(1) excluding output

    Args:
        nums: Input array

    Returns:
        Product array excluding self

    Examples:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    if len(nums) == 0:
        return []
    if len(nums) == 1:
        return [1]

    n = len(nums)
    output = [1] * n

    left_product = 1
    for i in range(n):
        output[i] = left_product
        left_product *= nums[i]

    right_product = 1
    for i in range(n - 1, -1, -1):
        output[i] *= right_product
        right_product *= nums[i]

    return output


def search_rotated_sorted(nums: list[int], target: int) -> int:
    """Search target in rotated sorted array.

    Time: O(log n), Space: O(1)

    Args:
        nums: Rotated sorted array with unique elements
        target: Target value to find

    Returns:
        Index of target, -1 if not found

    Examples:
        >>> search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 0)
        4
        >>> search_rotated_sorted([4, 5, 6, 7, 0, 1, 2], 3)
        -1
        >>> search_rotated_sorted([1], 0)
        -1
    """
    low = 0
    high = len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        if nums[low] <= nums[mid]:  # Left side is sorted
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:  # Right side is sorted
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1


def find_minimum_rotated(nums: list[int]) -> int:
    """Find minimum element in rotated sorted array.

    Time: O(log n), Space: O(1)

    Args:
        nums: Rotated sorted array

    Returns:
        Minimum element

    Examples:
        >>> find_minimum_rotated([3, 4, 5, 1, 2])
        1
        >>> find_minimum_rotated([4, 5, 6, 7, 0, 1, 2])
        0
        >>> find_minimum_rotated([11, 13, 15, 17])
        11
    """
    low = 0
    high = len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        if nums[mid] > nums[high]:
            low = mid + 1
        else:
            high = mid
    return nums[low]

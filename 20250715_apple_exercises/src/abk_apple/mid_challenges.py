"""
Mid Level Python Challenges for Apple Interview Preparation
"""


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Challenge: Group Anagrams
    Given an array of strings strs, group the anagrams together. You can return the answer in any order.
    An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase,
    typically using all the original letters exactly once.

    Example:
    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

    Time Complexity: O(n * k log k) where n is the number of strings and k is the maximum length
    Space Complexity: O(n * k)
    """
    if not strs:
        return []
    if len(strs) == 1:
        return [strs]

    result: list[list[str]] = []
    for i, s in enumerate(strs):
        if s == "":
            continue
        current_group = [s]
        for j in range(i + 1, len(strs)):
            if sorted(s) == sorted(strs[j]):
                current_group.append(strs[j])
                strs[j] = ""  # to eliminate already used item
        result.append(current_group)
    return result


def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Challenge: 3Sum
    Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
    such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
    Notice that the solution set must not contain duplicate triplets.

    Example:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]

    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    # Solution 1: complex but better O(n**), O(1)
    # if not nums:
    #     return []
    # if len(nums) < 3:
    #     return []
    # if len(nums) == 3:
    #     return [nums] if sum(nums) == 0 else []

    # nums.sort()
    # result: list[list[int]] = []
    # for i in range(len(nums) - 2):
    #     if i > 0 and nums[i] == nums[i - 1]:
    #         continue
    #     left, right = i + 1, len(nums) - 1
    #     while left < right:
    #         total = nums[i] + nums[left] + nums[right]
    #         if total == 0:
    #             result.append([nums[i], nums[left], nums[right]])
    #             while left < right and nums[left] == nums[left + 1]:
    #                 left += 1
    #             while left < right and nums[right] == nums[right - 1]:
    #                 right -= 1
    #             left += 1
    #             right -= 1
    #         elif total < 0:
    #             left += 1
    #         else:
    #             right -= 1
    # return result

    # Solution 2: simple but O(n**3), O(n)
    if not nums:
        return []
    result = set()  # Use set to avoid duplicates
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 0:
                    # Sort the triplet to handle duplicates
                    triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                    result.add(triplet)
    return [list(triplet) for triplet in result]


def longest_substring_without_repeating(s: str) -> int:
    """
    Challenge: Longest Substring Without Repeating Characters
    Given a string s, find the length of the longest substring without repeating characters.

    Example:
    Input: s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with the length of 3.

    Time Complexity: O(n)
    Space Complexity: O(min(m,n)) where m is the size of the charset
    """
    if not s:
        return 0
    if len(s) == 1:
        return 1

    char_set = set()
    max_length = 0
    left = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    return max_length


def valid_parentheses(s: str) -> bool:
    """
    Challenge: Valid Parentheses
    Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
    determine if the input string is valid.

    An input string is valid if:
    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.

    Example:
    Input: s = "()[]{}"
    Output: True

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    bracket_map = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in bracket_map.keys():  # Closing bracket
            if not stack or stack.pop() != bracket_map[char]:
                return False
        elif char in bracket_map.values():  # Opening bracket
            stack.append(char)
        # Ignore any other characters (letters, numbers, etc.)

    return len(stack) == 0


def product_except_self(nums: list[int]) -> list[int]:
    """
    Challenge: Product of Array Except Self
    Given an integer array nums, return an array answer such that answer[i] is equal to
    the product of all the elements of nums except nums[i].

    The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
    You must write an algorithm that runs in O(n) time and without using the division operation.

    Example:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not nums:
        return []
    if len(nums) == 1:
        return [1]

    # n = len(nums)
    # output = [1] * n
    # left_product = 1
    # for i in range(n):
    #     output[i] = left_product
    #     left_product *= nums[i]
    # right_product = 1
    # for i in range(n - 1, -1, -1):
    #     output[i] *= right_product
    #     right_product *= nums[i]
    # return output

    output: list[int] = []
    for i in range(len(nums)):
        exp_nums: list[int] = []
        product = 1
        exp_nums = nums[:i] + nums[i + 1 :]
        for j in exp_nums:
            product *= j
        output.append(product)
    return output


def max_subarray(nums: list[int]) -> int:
    """
    Challenge: Maximum Subarray (Kadane's Algorithm)
    Given an integer array nums, find the contiguous subarray (containing at least one number)
    which has the largest sum and return its sum.

    Example:
    Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
    Output: 6
    Explanation: [4,-1,2,1] has the largest sum = 6.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    max_sum = current_sum = nums[0]
    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    return max_sum


def rotate_array(nums: list[int], k: int) -> list[int]:
    """
    Challenge: Rotate Array
    Given an array, rotate the array to the right by k steps, where k is non-negative.

    Example:
    Input: nums = [1,2,3,4,5,6,7], k = 3
    Output: [5,6,7,1,2,3,4]
    Explanation: rotate 1 step to the right: [7,1,2,3,4,5,6]
                 rotate 2 steps to the right: [6,7,1,2,3,4,5]
                 rotate 3 steps to the right: [5,6,7,1,2,3,4]

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not nums or k <= 0:
        return nums
    k = k % len(nums)  # Handle cases where k is larger than n
    nums[:] = nums[-k:] + nums[:-k]  # Rotate in-place
    return nums

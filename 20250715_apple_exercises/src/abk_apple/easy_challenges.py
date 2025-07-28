"""
Easy Level Python Challenges for Apple Interview Preparation
"""


def two_sum(nums: list[int], target: int) -> list:
    """
    Challenge: Two Sum
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.

    Example:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    for i, n in enumerate(nums):
        if target - n in nums[i + 1 :]:
            return [i, nums.index(target - n, i + 1)]
    return []


def is_palindrome(s: str) -> bool:
    """
    Challenge: Valid Palindrome
    A phrase is a palindrome if, after converting all uppercase letters into lowercase letters
    and removing all non-alphanumeric characters, it reads the same forward and backward.

    Example:
    Input: s = "A man, a plan, a canal: Panama"
    Output: True
    Explanation: "amanaplanacanalpanama" is a palindrome.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    lower_case = s.lower()
    alphanumeric = "".join(char for char in lower_case if char.isalnum())
    return alphanumeric == alphanumeric[::-1]


def reverse_string(s: str) -> str:
    """
    Challenge: Reverse String
    Write a function that reverses a string. The input string is given as an array of characters s.
    You must do this by modifying the input array in-place with O(1) extra memory.

    Example:
    Input: s = ["h","e","l","l","o"]
    Output: ["o","l","l","e","h"]

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # solution 1
    # return s.reverse() # too easy

    # Solution 2
    left_index, right_index = 0, len(s) - 1
    while left_index < right_index:
        s[left_index], s[right_index] = s[right_index], s[left_index]
        left_index += 1
        right_index -= 1
    return s


def fizz_buzz(n: int) -> list[str]:
    """
    Challenge: Fizz Buzz
    Given an integer n, return a string array answer (1-indexed) where:
    - answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
    - answer[i] == "Fizz" if i is divisible by 3.
    - answer[i] == "Buzz" if i is divisible by 5.
    - answer[i] == i (as a string) otherwise.

    Example:
    Input: n = 3
    Output: ["1","2","Fizz"]

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if n < 1:
        return []

    result = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


def contains_duplicate(nums: list[int]) -> bool:
    """
    Challenge: Contains Duplicate
    Given an integer array nums, return true if any value appears at least twice in the array,
    and return false if every element is distinct.

    Example:
    Input: nums = [1,2,3,1]
    Output: True

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    set_converted = set(nums)
    return len(set_converted) != len(nums)

"""Group people functionality."""
#
# 1. People and IDs
#    - there are n people, labeled from 0 to n-1. The people have no names.
#      They are identified only by their position (index) within the input argument.
#
# 2. Input
#    - An integer array 'groupSizes' of length n.
#    - For each index i, 'groupSizes[i]' is the exact number of people that person i must be grouped with (including themselves).
#
# 3. Goal
#    - Partition all n people into one or more groups so that:
#      * Every group you form has exactly k members, where k is the required size for each member in that group.
#      * Each person appears in exactly one group.
#
# 4. Output
#    - Return any list of groups (each group is a list of person IDs) that satisfies the above requirements.
#    - The order of the groups, and the order of IDs within each group, does not matter.
#
# 5. Guarantee
#    - You can assume at least one valid grouping exists for the given input.
#
# Write an O(n)-time solution in Python3 below.
#
# Example:
# groupsSizes = [2, 1, 3, 3, 3, 2]
# Index:         0  1  2  3  4  5. (meaning, person 0, person 1, person 2, etc)
# Where the person in ""Index" is in group that is the size of the number listed above it in "groupSizes":
# - Person 0 -> group of size 2
# - Person 1 -> group of size 1
# - Person 2 -> group of size 3
# - Person 3 -> group of size 3
# - Person 4 -> group of size 3
# - Person 5 -> group of size 2
#
# One valid grouping/example answer (returned value):
# [
#    [1],       # person 1 is in a group of size 1
#    [0, 5],    # persons 0 and 5 are in a group of size 2
#    [2, 3, 4]  # persons 2, 3, and 4 are in a group of size 3
# ]
#
# Note: The order of groups and the order of IDs within each group may vary and are not relevant.
#
# Constraints:
# groupSizes.length == n
# 1 <= n <= 500
# 1 <= groupSizes[i] <= n
#
# Example 1:
# Input: groupSizes = [3,3,3,3,3,1,3]
# Output: [[5],[0,1,2],[3,4,6]]
#
# Example 2:
# Input: groupSizes = [2,1,3,3,3,2]
# Output: [[1],[0,5],[2,3,4]]


def group_people(group_sizes: list[int]) -> list[list[int]]:
    """Group people functionality."""
    groups = {}
    for i, size in enumerate(group_sizes):
        # if size not in groups:
        #     groups[size] = []
        # groups[size].append(i)
        groups.setdefault(size, []).append(i)

    result = []
    for size, people in groups.items():
        for i in range(0, len(people), size):
            result.append(people[i : i + size])

    return result


def group_people_v2(group_sizes: list[int]) -> list[list[int]]:
    """Group people functionality."""
    if not group_sizes:
        return []

    groups = {}
    result_list: list[list[int]] = []
    for i, size in enumerate(group_sizes):
        groups.setdefault(size, []).append(i)
        if len(groups[size]) == size:
            result_list.append(groups[size])
            groups[size] = []
    return result_list

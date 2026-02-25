"""Advanced array algorithms for interview preparation."""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals.

    Time: O(n log n), Space: O(1) excluding output

    Args:
        intervals: List of intervals [start, end]

    Returns:
        Merged intervals

    Examples:
        >>> merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
        [[1, 6], [8, 10], [15, 18]]
        >>> merge_intervals([[1, 4], [4, 5]])
        [[1, 5]]
        >>> merge_intervals([[1, 4], [0, 4]])
        [[0, 4]]
    """
    if not intervals:
        return []

    # Sort intervals by start time
    intervals.sort(key=lambda x: x[0])

    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]

        # If current interval overlaps with last merged interval
        if current[0] <= last[1]:
            # Merge by updating end time
            last[1] = max(last[1], current[1])
        else:
            # No overlap, add current interval
            merged.append(current)

    return merged


def insert_interval(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    """Insert interval into sorted non-overlapping intervals.

    Time: O(n), Space: O(1) excluding output

    Args:
        intervals: Sorted non-overlapping intervals
        newInterval: Interval to insert

    Returns:
        Merged intervals after insertion

    Examples:
        >>> insert_interval([[1, 3], [6, 9]], [2, 5])
        [[1, 5], [6, 9]]
        >>> insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8])
        [[1, 2], [3, 10], [12, 16]]
    """
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals before newInterval
    while i < n and intervals[i][1] < newInterval[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= newInterval[1]:
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i += 1

    # Add merged interval
    result.append(newInterval)

    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


def non_overlapping_intervals(intervals: list[list[int]]) -> int:
    """Find minimum intervals to remove to make rest non-overlapping.

    Time: O(n log n), Space: O(1)

    Args:
        intervals: List of intervals

    Returns:
        Minimum intervals to remove

    Examples:
        >>> non_overlapping_intervals([[1, 2], [2, 3], [3, 4], [1, 3]])
        1
        >>> non_overlapping_intervals([[1, 2], [1, 2], [1, 2]])
        2
        >>> non_overlapping_intervals([[1, 2], [2, 3]])
        0
    """
    if not intervals:
        return 0

    # Sort by end time (greedy approach)
    intervals.sort(key=lambda x: x[1])

    count = 0
    end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            # Overlapping interval, need to remove it
            count += 1
        else:
            # Non-overlapping, update end time
            end = intervals[i][1]

    return count


def meeting_rooms_ii(intervals: list[list[int]]) -> int:
    """Find minimum number of meeting rooms required.

    Time: O(n log n), Space: O(n)

    Args:
        intervals: Meeting time intervals [start, end]

    Returns:
        Minimum rooms needed

    Examples:
        >>> meeting_rooms_ii([[0, 30], [5, 10], [15, 20]])
        2
        >>> meeting_rooms_ii([[7, 10], [2, 4]])
        1
        >>> meeting_rooms_ii([[9, 10], [4, 9], [4, 17]])
        2
    """
    if not intervals:
        return 0

    import heapq

    # Sort by start time
    intervals.sort()

    # Min heap to track end times of ongoing meetings
    min_heap = []

    for start, end in intervals:
        # Remove meetings that have ended
        while min_heap and min_heap[0] <= start:
            heapq.heappop(min_heap)

        # Add current meeting's end time
        heapq.heappush(min_heap, end)

    return len(min_heap)


def spiral_matrix(matrix: list[list[int]]) -> list[int]:
    """Return matrix elements in spiral order.

    Time: O(m * n), Space: O(1) excluding output

    Args:
        matrix: m x n matrix

    Returns:
        Elements in spiral order

    Examples:
        >>> spiral_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [1, 2, 3, 6, 9, 8, 7, 4, 5]
        >>> spiral_matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    """
    if not matrix or not matrix[0]:
        return []

    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1

        # Traverse down
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1

        # Traverse left (if we still have rows)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1

        # Traverse up (if we still have columns)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1

    return result


def generate_spiral_matrix(n: int) -> list[list[int]]:
    """Generate n x n matrix filled in spiral order.

    Time: O(n²), Space: O(1) excluding output

    Args:
        n: Size of matrix

    Returns:
        n x n matrix filled 1 to n² in spiral order

    Examples:
        >>> generate_spiral_matrix(3)
        [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
        >>> generate_spiral_matrix(1)
        [[1]]
    """
    matrix = [[0] * n for _ in range(n)]

    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1

    while top <= bottom and left <= right:
        # Fill right
        for col in range(left, right + 1):
            matrix[top][col] = num
            num += 1
        top += 1

        # Fill down
        for row in range(top, bottom + 1):
            matrix[row][right] = num
            num += 1
        right -= 1

        # Fill left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                matrix[bottom][col] = num
                num += 1
            bottom -= 1

        # Fill up
        if left <= right:
            for row in range(bottom, top - 1, -1):
                matrix[row][left] = num
                num += 1
            left += 1

    return matrix


def rotate_matrix_90(matrix: list[list[int]]) -> None:
    """Rotate n x n matrix 90 degrees clockwise in-place.

    Time: O(n²), Space: O(1)

    Args:
        matrix: n x n matrix to rotate in-place

    Examples:
        >>> matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> rotate_matrix_90(matrix)
        >>> matrix
        [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    n = len(matrix)

    # Transpose the matrix
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Reverse each row
    for i in range(n):
        matrix[i].reverse()


def set_matrix_zeros(matrix: list[list[int]]) -> None:
    """Set entire row and column to 0 if element is 0.

    Time: O(m * n), Space: O(1)

    Args:
        matrix: m x n matrix to modify in-place

    Examples:
        >>> matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        >>> set_matrix_zeros(matrix)
        >>> matrix
        [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    """
    if not matrix or not matrix[0]:
        return

    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use first row and column as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[0][j] = 0
                matrix[i][0] = 0

    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[0][j] == 0 or matrix[i][0] == 0:
                matrix[i][j] = 0

    # Handle first row and column
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0

    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0


def search_2d_matrix(matrix: list[list[int]], target: int) -> bool:
    """Search target in sorted 2D matrix.

    Time: O(log(m * n)), Space: O(1)

    Args:
        matrix: Sorted matrix (each row sorted, first element of each row > last of previous)
        target: Target value

    Returns:
        True if target found

    Examples:
        >>> search_2d_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3)
        True
        >>> search_2d_matrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13)
        False
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1

    while left <= right:
        mid = (left + right) // 2
        mid_val = matrix[mid // n][mid % n]

        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def search_2d_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    """Search target in row and column wise sorted matrix.

    Time: O(m + n), Space: O(1)

    Args:
        matrix: Matrix sorted row-wise and column-wise
        target: Target value

    Returns:
        True if target found

    Examples:
        >>> matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
        >>> search_2d_matrix_ii(matrix, 5)
        True
        >>> search_2d_matrix_ii(matrix, 20)
        False
    """
    if not matrix or not matrix[0]:
        return False

    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1

    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False


def find_peak_element(nums: list[int]) -> int:
    """Find peak element index (element greater than neighbors).

    Time: O(log n), Space: O(1)

    Args:
        nums: Array where nums[i] != nums[i+1]

    Returns:
        Index of any peak element

    Examples:
        >>> find_peak_element([1, 2, 3, 1])
        2
        >>> find_peak_element([1, 2, 1, 3, 5, 6, 4])
        5
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[mid + 1]:
            # Peak is on the left side (including mid)
            right = mid
        else:
            # Peak is on the right side
            left = mid + 1

    return left


def first_missing_positive(nums: list[int]) -> int:
    """Find smallest missing positive integer.

    Time: O(n), Space: O(1)

    Args:
        nums: Array of integers

    Returns:
        Smallest missing positive integer

    Examples:
        >>> first_missing_positive([1, 2, 0])
        3
        >>> first_missing_positive([3, 4, -1, 1])
        2
        >>> first_missing_positive([7, 8, 9, 11, 12])
        1
    """
    n = len(nums)

    # Mark numbers (num < 1 or num > n) as out of range
    for i in range(n):
        if nums[i] < 1 or nums[i] > n:
            nums[i] = n + 1

    # Mark existence of number by negating value at index
    for i in range(n):
        num = abs(nums[i])
        if num <= n:
            nums[num - 1] = -abs(nums[num - 1])

    # Find first positive value (missing number)
    for i in range(n):
        if nums[i] > 0:
            return i + 1

    return n + 1


def trapping_rain_water(height: list[int]) -> int:
    """Calculate trapped rainwater.

    Time: O(n), Space: O(1)

    Args:
        height: Array representing elevation map

    Returns:
        Units of trapped rainwater

    Examples:
        >>> trapping_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
        6
        >>> trapping_rain_water([4, 2, 0, 3, 2, 5])
        9
    """
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water


def candy_distribution(ratings: list[int]) -> int:
    """Minimum candies to distribute based on ratings.

    Time: O(n), Space: O(1)

    Args:
        ratings: Children's ratings

    Returns:
        Minimum candies needed

    Examples:
        >>> candy_distribution([1, 0, 2])
        5
        >>> candy_distribution([1, 2, 2])
        4
        >>> candy_distribution([1, 3, 2, 2, 1])
        7
    """
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n

    # Forward pass: left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Backward pass: right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


def gas_station_circuit(gas: list[int], cost: list[int]) -> int:
    """Find starting gas station to complete circuit.

    Time: O(n), Space: O(1)

    Args:
        gas: Gas available at each station
        cost: Cost to travel to next station

    Returns:
        Starting station index, -1 if impossible

    Examples:
        >>> gas_station_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
        3
        >>> gas_station_circuit([2, 3, 4], [3, 4, 3])
        -1
    """
    total_tank = 0
    curr_tank = 0
    start_station = 0

    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        curr_tank += gas[i] - cost[i]

        # If we can't reach the next station
        if curr_tank < 0:
            start_station = i + 1
            curr_tank = 0

    return start_station if total_tank >= 0 else -1


def h_index(citations: list[int]) -> int:
    """Calculate H-Index from citation counts.

    Time: O(n log n), Space: O(1)

    Args:
        citations: Citation counts for papers

    Returns:
        H-Index value

    Examples:
        >>> h_index([3, 0, 6, 1, 5])
        3
        >>> h_index([1, 3, 1])
        1
        >>> h_index([100])
        1
    """
    citations.sort(reverse=True)
    h = 0

    for i, citation in enumerate(citations):
        # At least i+1 papers with citation >= citation
        if citation >= i + 1:
            h = i + 1
        else:
            break

    return h

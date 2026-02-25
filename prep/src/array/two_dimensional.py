"""Two-dimensional array problems for interview preparation."""


def number_of_islands(grid: list[list[str]]) -> int:
    """Count number of islands in 2D grid.

    Time: O(m * n), Space: O(m * n) for recursion stack

    Args:
        grid: 2D grid where '1' is land, '0' is water

    Returns:
        Number of islands

    Examples:
        >>> number_of_islands(
        ...     [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
        ... )
        1
        >>> number_of_islands(
        ...     [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
        ... )
        3
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    count = 0

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == "0":
            return

        grid[i][j] = "0"  # Mark as visited

        # Explore all 4 directions
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == "1":
                count += 1
                dfs(i, j)

    return count


def max_area_island(grid: list[list[int]]) -> int:
    """Find maximum area of island.

    Time: O(m * n), Space: O(m * n)

    Args:
        grid: 2D grid where 1 is land, 0 is water

    Returns:
        Maximum area of any island

    Examples:
        >>> max_area_island(
        ...     [
        ...         [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ...         [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        ...         [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ...     ]
        ... )
        6
        >>> max_area_island([[0, 0, 0, 0, 0, 0, 0, 0]])
        0
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    max_area = 0

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] == 0:
            return 0

        grid[i][j] = 0  # Mark as visited

        # Count current cell + all connected cells
        return 1 + dfs(i + 1, j) + dfs(i - 1, j) + dfs(i, j + 1) + dfs(i, j - 1)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                max_area = max(max_area, dfs(i, j))

    return max_area


def surrounded_regions(board: list[list[str]]) -> None:
    """Capture surrounded regions on board.

    Time: O(m * n), Space: O(m * n)

    Args:
        board: 2D board with 'X' and 'O', modify in-place

    Examples:
        >>> board = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]
        >>> surrounded_regions(board)
        >>> board
        [['X','X','X','X'],['X','X','X','X'],['X','X','X','X'],['X','O','X','X']]
    """
    if not board or not board[0]:
        return

    m, n = len(board), len(board[0])

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != "O":
            return

        board[i][j] = "T"  # Mark as temporary

        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    # Mark all 'O's connected to border as 'T'
    for i in range(m):
        if board[i][0] == "O":
            dfs(i, 0)
        if board[i][n - 1] == "O":
            dfs(i, n - 1)

    for j in range(n):
        if board[0][j] == "O":
            dfs(0, j)
        if board[m - 1][j] == "O":
            dfs(m - 1, j)

    # Convert remaining 'O's to 'X' and 'T's back to 'O'
    for i in range(m):
        for j in range(n):
            if board[i][j] == "O":
                board[i][j] = "X"
            elif board[i][j] == "T":
                board[i][j] = "O"


def pacific_atlantic_water(heights: list[list[int]]) -> list[list[int]]:
    """Find cells where water can flow to both Pacific and Atlantic oceans.

    Time: O(m * n), Space: O(m * n)

    Args:
        heights: Matrix of heights

    Returns:
        List of coordinates that can reach both oceans

    Examples:
        >>> pacific_atlantic_water([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]])
        [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    """
    if not heights or not heights[0]:
        return []

    m, n = len(heights), len(heights[0])
    pacific = [[False] * n for _ in range(m)]
    atlantic = [[False] * n for _ in range(m)]

    def dfs(i, j, visited, prev_height):
        if i < 0 or i >= m or j < 0 or j >= n or visited[i][j] or heights[i][j] < prev_height:
            return

        visited[i][j] = True

        dfs(i + 1, j, visited, heights[i][j])
        dfs(i - 1, j, visited, heights[i][j])
        dfs(i, j + 1, visited, heights[i][j])
        dfs(i, j - 1, visited, heights[i][j])

    # Start from Pacific borders (top and left)
    for i in range(m):
        dfs(i, 0, pacific, heights[i][0])
        dfs(i, n - 1, atlantic, heights[i][n - 1])

    for j in range(n):
        dfs(0, j, pacific, heights[0][j])
        dfs(m - 1, j, atlantic, heights[m - 1][j])

    # Find cells that can reach both oceans
    result = []
    for i in range(m):
        for j in range(n):
            if pacific[i][j] and atlantic[i][j]:
                result.append([i, j])

    return result


def word_search(board: list[list[str]], word: str) -> bool:
    """Search for word in 2D board.

    Time: O(m * n * 4^L), Space: O(L) where L is word length

    Args:
        board: 2D board of characters
        word: Word to search

    Returns:
        True if word exists in board

    Examples:
        >>> board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        >>> word_search(board, "ABCCED")
        True
        >>> word_search(board, "SEE")
        True
        >>> word_search(board, "ABCB")
        False
    """
    if not board or not board[0]:
        return False
    if not word:
        return True

    m, n = len(board), len(board[0])

    def dfs(i, j, idx):
        if idx == len(word):
            return True

        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[idx]:
            return False

        # Mark as visited
        temp = board[i][j]
        board[i][j] = "#"

        # Explore all 4 directions
        found = dfs(i + 1, j, idx + 1) or dfs(i - 1, j, idx + 1) or dfs(i, j + 1, idx + 1) or dfs(i, j - 1, idx + 1)

        # Restore original character
        board[i][j] = temp

        return found

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True

    return False


def word_search_ii(board: list[list[str]], words: list[str]) -> list[str]:
    """Find all words in 2D board.

    Time: O(m * n * 4^L * W), Space: O(W * L)

    Args:
        board: 2D board of characters
        words: List of words to search

    Returns:
        List of words found in board

    Examples:
        >>> board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
        >>> word_search_ii(board, ["oath", "pea", "eat", "rain"])
        ['eat', 'oath']
    """
    if not board or not board[0] or not words:
        return []

    result = []
    for word in words:
        if word_search(board, word):
            result.append(word)

    return result


def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """Find shortest path in binary matrix from top-left to bottom-right.

    Time: O(n²), Space: O(n²)

    Args:
        grid: Binary matrix where 0 is walkable, 1 is blocked

    Returns:
        Shortest path length, -1 if no path

    Examples:
        >>> shortest_path_binary_matrix([[0, 1], [1, 0]])
        2
        >>> shortest_path_binary_matrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]])
        4
        >>> shortest_path_binary_matrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]])
        -1
    """
    if not grid or not grid[0] or grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1

    n = len(grid)
    if n == 1:
        return 1 if grid[0][0] == 0 else -1

    from collections import deque

    queue = deque([(0, 0, 1)])  # (row, col, path_length)
    visited = set()
    visited.add((0, 0))

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    while queue:
        row, col, path_length = queue.popleft()

        if row == n - 1 and col == n - 1:
            return path_length

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < n and 0 <= new_col < n and grid[new_row][new_col] == 0 and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, path_length + 1))

    return -1


def walls_and_gates(rooms: list[list[int]]) -> None:
    """Fill rooms with distance to nearest gate.

    Time: O(m * n), Space: O(m * n)

    Args:
        rooms: Matrix where -1 is wall, 0 is gate, INF is empty room

    Examples:
        >>> INF = 2147483647
        >>> rooms = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
        >>> walls_and_gates(rooms)
        >>> rooms
        [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
    """
    if not rooms or not rooms[0]:
        return

    m, n = len(rooms), len(rooms[0])
    from collections import deque

    queue = deque()

    # Find all gates and add them to queue
    for i in range(m):
        for j in range(n):
            if rooms[i][j] == 0:
                queue.append((i, j, 0))

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        row, col, dist = queue.popleft()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < m and 0 <= new_col < n and rooms[new_row][new_col] > dist + 1:
                rooms[new_row][new_col] = dist + 1
                queue.append((new_row, new_col, dist + 1))


def count_battleships(board: list[list[str]]) -> int:
    """Count battleships in board.

    Time: O(m * n), Space: O(1)

    Args:
        board: Board where 'X' is battleship, '.' is water

    Returns:
        Number of battleships

    Examples:
        >>> count_battleships([["X", ".", ".", "X"], [".", ".", ".", "X"], [".", ".", ".", "X"]])
        2
        >>> count_battleships([["."]])
        0
    """
    if not board or not board[0]:
        return 0

    m, n = len(board), len(board[0])
    count = 0

    for i in range(m):
        for j in range(n):
            if board[i][j] == "X" and (i == 0 or board[i - 1][j] == ".") and (j == 0 or board[i][j - 1] == "."):
                # This is the top-left corner of a battleship
                count += 1

    return count


def unique_paths_with_obstacles_2d(obstacleGrid: list[list[int]]) -> int:
    """Count unique paths avoiding obstacles.

    Time: O(m * n), Space: O(1)

    Args:
        obstacleGrid: Grid where 1 is obstacle, 0 is free

    Returns:
        Number of unique paths

    Examples:
        >>> unique_paths_with_obstacles_2d([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        2
        >>> unique_paths_with_obstacles_2d([[0, 1], [0, 0]])
        1
    """
    if not obstacleGrid or not obstacleGrid[0] or obstacleGrid[0][0] == 1:
        return 0

    m, n = len(obstacleGrid), len(obstacleGrid[0])

    # Use the obstacle grid itself for DP to save space
    obstacleGrid[0][0] = 1

    # Initialize first row
    for j in range(1, n):
        obstacleGrid[0][j] = obstacleGrid[0][j - 1] if obstacleGrid[0][j] == 0 else 0

    # Initialize first column
    for i in range(1, m):
        obstacleGrid[i][0] = obstacleGrid[i - 1][0] if obstacleGrid[i][0] == 0 else 0

    # Fill the rest of the grid
    for i in range(1, m):
        for j in range(1, n):
            if obstacleGrid[i][j] == 1:
                obstacleGrid[i][j] = 0
            else:
                obstacleGrid[i][j] = obstacleGrid[i - 1][j] + obstacleGrid[i][j - 1]

    return obstacleGrid[m - 1][n - 1]


def maximal_rectangle(matrix: list[list[str]]) -> int:
    """Find largest rectangle containing only 1s.

    Time: O(m * n), Space: O(n)

    Args:
        matrix: Binary matrix with '0' and '1'

    Returns:
        Area of largest rectangle

    Examples:
        >>> maximal_rectangle(
        ...     [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
        ... )
        6
        >>> maximal_rectangle([["0"]])
        0
        >>> maximal_rectangle([["1"]])
        1
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix[0])
    heights = [0] * n
    max_area = 0

    for row in matrix:
        for j in range(n):
            if row[j] == "1":
                heights[j] += 1
            else:
                heights[j] = 0

        max_area = max(max_area, largest_rectangle_histogram(heights))

    return max_area


def largest_rectangle_histogram(heights: list[int]) -> int:
    """Find largest rectangle in histogram.

    Time: O(n), Space: O(n)

    Args:
        heights: Heights of histogram bars

    Returns:
        Area of largest rectangle

    Examples:
        >>> largest_rectangle_histogram([2, 1, 5, 6, 2, 3])
        10
        >>> largest_rectangle_histogram([2, 4])
        4
        >>> largest_rectangle_histogram([1, 1])
        2
    """
    if not heights:
        return 0

    stack = []
    max_area = 0

    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * width)

        stack.append(i)

    # Process remaining bars in stack
    while stack:
        h = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, h * width)

    return max_area


def game_of_life(board: list[list[int]]) -> None:
    """Apply Game of Life rules to board.

    Time: O(m * n), Space: O(1)

    Args:
        board: Board to update in-place (0 dead, 1 alive)

    Examples:
        >>> board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
        >>> game_of_life(board)
        >>> board
        [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]
    """
    if not board or not board[0]:
        return

    m, n = len(board), len(board[0])

    # Use additional states to track changes in-place
    # 0: dead -> dead
    # 1: live -> live
    # 2: live -> dead
    # 3: dead -> live

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(m):
        for j in range(n):
            live_neighbors = 0

            # Count live neighbors
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in [1, 2]:
                    live_neighbors += 1

            # Apply rules
            if board[i][j] == 1:  # Currently live
                if live_neighbors < 2 or live_neighbors > 3:
                    board[i][j] = 2  # Will die
            else:  # Currently dead
                if live_neighbors == 3:
                    board[i][j] = 3  # Will become alive

    # Update to final states
    for i in range(m):
        for j in range(n):
            if board[i][j] == 2:
                board[i][j] = 0
            elif board[i][j] == 3:
                board[i][j] = 1


def shortest_distance_buildings(grid: list[list[int]]) -> int:
    """Find shortest distance to build house accessible to all buildings.

    Time: O(m² * n²), Space: O(m * n)

    Args:
        grid: Grid where 0 is land, 1 is building, 2 is obstacle

    Returns:
        Minimum total distance, -1 if impossible

    Examples:
        >>> shortest_distance_buildings([[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]])
        7
    """
    if not grid or not grid[0]:
        return -1

    m, n = len(grid), len(grid[0])
    from collections import deque

    # Count total buildings
    buildings = []
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                buildings.append((i, j))

    if not buildings:
        return 0

    # Total distance and reachability count for each empty cell
    total_dist = [[0] * n for _ in range(m)]
    reach_count = [[0] * n for _ in range(m)]

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # BFS from each building
    for _building_idx, (start_i, start_j) in enumerate(buildings):
        queue = deque([(start_i, start_j, 0)])
        visited = set()
        visited.add((start_i, start_j))

        while queue:
            i, j, dist = queue.popleft()

            for di, dj in directions:
                ni, nj = i + di, j + dj

                if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in visited and grid[ni][nj] == 0:
                    visited.add((ni, nj))
                    total_dist[ni][nj] += dist + 1
                    reach_count[ni][nj] += 1
                    queue.append((ni, nj, dist + 1))

    # Find minimum distance among cells reachable by all buildings
    min_dist = float("inf")
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0 and reach_count[i][j] == len(buildings):
                min_dist = min(min_dist, total_dist[i][j])

    return min_dist if min_dist != float("inf") else -1


def island_perimeter(grid: list[list[int]]) -> int:
    """Calculate perimeter of island.

    Time: O(m * n), Space: O(1)

    Args:
        grid: Grid where 1 is land, 0 is water

    Returns:
        Perimeter of the island

    Examples:
        >>> island_perimeter([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]])
        16
        >>> island_perimeter([[1]])
        4
        >>> island_perimeter([[1, 0]])
        4
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    perimeter = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                # Start with 4 sides
                sides = 4

                # Check adjacent cells
                if i > 0 and grid[i - 1][j] == 1:  # Top
                    sides -= 1
                if i < m - 1 and grid[i + 1][j] == 1:  # Bottom
                    sides -= 1
                if j > 0 and grid[i][j - 1] == 1:  # Left
                    sides -= 1
                if j < n - 1 and grid[i][j + 1] == 1:  # Right
                    sides -= 1

                perimeter += sides

    return perimeter

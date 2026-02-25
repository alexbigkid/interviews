"""Tests for two-dimensional array problems."""

from src.array.two_dimensional import (
    number_of_islands,
    max_area_island,
    surrounded_regions,
    pacific_atlantic_water,
    word_search,
    word_search_ii,
    shortest_path_binary_matrix,
    walls_and_gates,
    count_battleships,
    unique_paths_with_obstacles_2d,
    maximal_rectangle,
    largest_rectangle_histogram,
    game_of_life,
    shortest_distance_buildings,
    island_perimeter,
)


class TestNumberOfIslands:
    """Test number_of_islands function."""

    def test_single_island(self):
        grid = [["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]]
        assert number_of_islands(grid) == 1

    def test_multiple_islands(self):
        grid = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
        assert number_of_islands(grid) == 3

    def test_no_islands(self):
        grid = [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]
        assert number_of_islands(grid) == 0

    def test_all_islands(self):
        grid = [["1", "1"], ["1", "1"]]
        assert number_of_islands(grid) == 1

    def test_single_cell_island(self):
        grid = [["1"]]
        assert number_of_islands(grid) == 1

    def test_single_cell_water(self):
        grid = [["0"]]
        assert number_of_islands(grid) == 0


class TestMaxAreaIsland:
    """Test max_area_island function."""

    def test_no_islands(self):
        grid = [[0, 0, 0, 0, 0, 0, 0, 0]]
        assert max_area_island(grid) == 0

    def test_single_cell_island(self):
        grid = [[1]]
        assert max_area_island(grid) == 1

    def test_multiple_equal_islands(self):
        grid = [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 1]]
        assert max_area_island(grid) == 4

    def test_single_row_island(self):
        grid = [[1, 1, 1, 1, 1]]
        assert max_area_island(grid) == 5


class TestSurroundedRegions:
    """Test surrounded_regions function."""

    def test_simple_case(self):
        board = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]
        surrounded_regions(board)
        expected = [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]
        assert board == expected

    def test_no_surrounded_regions(self):
        board = [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
        original = [row[:] for row in board]  # Deep copy
        surrounded_regions(board)
        assert board == original

    def test_border_regions(self):
        board = [["O", "X", "X", "O", "X"], ["X", "O", "O", "X", "O"], ["X", "O", "X", "O", "X"], ["O", "X", "O", "O", "O"]]
        surrounded_regions(board)
        # Border O's should remain, only completely surrounded O's become X
        assert board[1][1] == "X" and board[1][2] == "X"  # These should be captured

    def test_single_cell(self):
        board = [["O"]]
        surrounded_regions(board)
        assert board == [["O"]]  # Border cell, not surrounded


class TestPacificAtlanticWater:
    """Test pacific_atlantic_water function."""

    def test_simple_case(self):
        heights = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
        result = pacific_atlantic_water(heights)
        expected = [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
        assert sorted(result) == sorted(expected)

    def test_single_cell(self):
        heights = [[1]]
        result = pacific_atlantic_water(heights)
        assert result == [[0, 0]]

    def test_all_same_height(self):
        heights = [[1, 1], [1, 1]]
        result = pacific_atlantic_water(heights)
        assert len(result) == 4  # All cells should reach both oceans

    def test_increasing_heights(self):
        heights = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = pacific_atlantic_water(heights)
        # Only the highest points should reach both oceans
        assert [2, 2] in result


class TestWordSearch:
    """Test word_search function."""

    def test_word_exists(self):
        board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        assert word_search(board, "ABCCED")

    def test_another_word_exists(self):
        board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        assert word_search(board, "SEE")

    def test_word_not_exists(self):
        board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
        assert not word_search(board, "ABCB")

    def test_single_cell_match(self):
        board = [["A"]]
        assert word_search(board, "A")

    def test_single_cell_no_match(self):
        board = [["A"]]
        assert not word_search(board, "B")

    def test_empty_word(self):
        board = [["A", "B"], ["C", "D"]]
        assert word_search(board, "")


class TestWordSearchII:
    """Test word_search_ii function."""

    def test_multiple_words(self):
        board = [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]]
        words = ["oath", "pea", "eat", "rain"]
        result = word_search_ii(board, words)
        assert sorted(result) == sorted(["eat", "oath"])

    def test_no_words_found(self):
        board = [["a", "b"], ["c", "d"]]
        words = ["xyz", "abc"]
        result = word_search_ii(board, words)
        assert "xyz" not in result

    def test_single_word(self):
        board = [["a", "a"]]
        words = ["aa"]
        result = word_search_ii(board, words)
        assert result == ["aa"]

    def test_empty_words_list(self):
        board = [["a", "b"], ["c", "d"]]
        words = []
        result = word_search_ii(board, words)
        assert result == []


class TestShortestPathBinaryMatrix:
    """Test shortest_path_binary_matrix function."""

    def test_simple_path(self):
        grid = [[0, 1], [1, 0]]
        assert shortest_path_binary_matrix(grid) == 2

    def test_longer_path(self):
        grid = [[0, 0, 0], [1, 1, 0], [1, 1, 0]]
        assert shortest_path_binary_matrix(grid) == 4

    def test_no_path(self):
        grid = [[1, 0, 0], [1, 1, 0], [1, 1, 0]]
        assert shortest_path_binary_matrix(grid) == -1

    def test_single_cell_clear(self):
        grid = [[0]]
        assert shortest_path_binary_matrix(grid) == 1

    def test_single_cell_blocked(self):
        grid = [[1]]
        assert shortest_path_binary_matrix(grid) == -1

    def test_already_at_destination(self):
        grid = [[0]]
        assert shortest_path_binary_matrix(grid) == 1


class TestWallsAndGates:
    """Test walls_and_gates function."""

    def test_simple_case(self):
        INF = 2147483647
        rooms = [[INF, -1, 0, INF], [INF, INF, INF, -1], [INF, -1, INF, -1], [0, -1, INF, INF]]
        walls_and_gates(rooms)
        expected = [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
        assert rooms == expected

    def test_no_gates(self):
        INF = 2147483647
        rooms = [[INF, INF, INF], [-1, -1, -1], [INF, INF, INF]]
        original = [row[:] for row in rooms]
        walls_and_gates(rooms)
        assert rooms == original  # Should remain unchanged

    def test_all_gates(self):
        rooms = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        walls_and_gates(rooms)
        assert rooms == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # All remain 0

    def test_single_gate(self):
        rooms = [[0]]
        walls_and_gates(rooms)
        assert rooms == [[0]]


class TestCountBattleships:
    """Test count_battleships function."""

    def test_simple_case(self):
        board = [["X", ".", ".", "X"], [".", ".", ".", "X"], [".", ".", ".", "X"]]
        assert count_battleships(board) == 2

    def test_no_battleships(self):
        board = [["."]]
        assert count_battleships(board) == 0

    def test_single_battleship(self):
        board = [["X"]]
        assert count_battleships(board) == 1

    def test_multiple_isolated_battleships(self):
        board = [["X", ".", "X"], [".", ".", "."], ["X", ".", "X"]]
        assert count_battleships(board) == 4

    def test_long_battleship(self):
        board = [["X", "X", "X", "X"]]
        assert count_battleships(board) == 1


class TestUniquePathsWithObstacles2D:
    """Test unique_paths_with_obstacles_2d function."""

    def test_simple_case(self):
        grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        assert unique_paths_with_obstacles_2d(grid) == 2

    def test_blocked_path(self):
        grid = [[0, 1], [0, 0]]
        assert unique_paths_with_obstacles_2d(grid) == 1

    def test_start_blocked(self):
        grid = [[1, 0], [0, 0]]
        assert unique_paths_with_obstacles_2d(grid) == 0

    def test_end_blocked(self):
        grid = [[0, 0], [0, 1]]
        assert unique_paths_with_obstacles_2d(grid) == 0

    def test_no_obstacles(self):
        grid = [[0, 0], [0, 0]]
        assert unique_paths_with_obstacles_2d(grid) == 2


class TestMaximalRectangle:
    """Test maximal_rectangle function."""

    def test_simple_case(self):
        matrix = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
        assert maximal_rectangle(matrix) == 6

    def test_single_zero(self):
        matrix = [["0"]]
        assert maximal_rectangle(matrix) == 0

    def test_single_one(self):
        matrix = [["1"]]
        assert maximal_rectangle(matrix) == 1

    def test_all_ones(self):
        matrix = [["1", "1"], ["1", "1"]]
        assert maximal_rectangle(matrix) == 4

    def test_single_row(self):
        matrix = [["1", "1", "1", "1"]]
        assert maximal_rectangle(matrix) == 4


class TestLargestRectangleHistogram:
    """Test largest_rectangle_histogram function."""

    def test_simple_case(self):
        assert largest_rectangle_histogram([2, 1, 5, 6, 2, 3]) == 10

    def test_increasing_heights(self):
        assert largest_rectangle_histogram([2, 4]) == 4

    def test_equal_heights(self):
        assert largest_rectangle_histogram([1, 1]) == 2

    def test_single_bar(self):
        assert largest_rectangle_histogram([5]) == 5

    def test_decreasing_heights(self):
        assert largest_rectangle_histogram([6, 5, 4, 3, 2, 1]) == 12

    def test_all_same_height(self):
        assert largest_rectangle_histogram([3, 3, 3, 3]) == 12


class TestGameOfLife:
    """Test game_of_life function."""

    def test_simple_case(self):
        board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
        game_of_life(board)
        expected = [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]
        assert board == expected

    def test_single_cell_dies(self):
        board = [[1]]
        game_of_life(board)
        assert board == [[0]]  # Single cell dies from isolation

    def test_stable_pattern(self):
        board = [[1, 1], [1, 1]]
        game_of_life(board)
        assert board == [[1, 1], [1, 1]]  # 2x2 block is stable

    def test_all_dead(self):
        board = [[0, 0], [0, 0]]
        game_of_life(board)
        assert board == [[0, 0], [0, 0]]  # Remains dead


class TestShortestDistanceBuildings:
    """Test shortest_distance_buildings function."""

    def test_simple_case(self):
        grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]
        result = shortest_distance_buildings(grid)
        assert result == 7

    def test_single_building(self):
        grid = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        result = shortest_distance_buildings(grid)
        assert result >= 0  # Should find some valid location

    def test_no_buildings(self):
        grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        result = shortest_distance_buildings(grid)
        assert result == 0  # No buildings to reach


class TestIslandPerimeter:
    """Test island_perimeter function."""

    def test_simple_case(self):
        grid = [[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]
        assert island_perimeter(grid) == 16

    def test_single_cell(self):
        grid = [[1]]
        assert island_perimeter(grid) == 4

    def test_single_row(self):
        grid = [[1, 0]]
        assert island_perimeter(grid) == 4

    def test_no_island(self):
        grid = [[0, 0], [0, 0]]
        assert island_perimeter(grid) == 0

    def test_full_square(self):
        grid = [[1, 1], [1, 1]]
        assert island_perimeter(grid) == 8

    def test_l_shape(self):
        grid = [[1, 1, 0], [1, 0, 0], [0, 0, 0]]
        assert island_perimeter(grid) == 8

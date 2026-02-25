"""Tests for dynamic programming array problems."""

from src.array.dynamic_programming import (
    coin_change,
    coin_change_combinations,
    longest_increasing_subsequence,
    longest_increasing_subsequence_sequence,
    maximum_product_subarray,
    house_robber,
    house_robber_circular,
    jump_game,
    jump_game_min_jumps,
    unique_paths_grid,
    unique_paths_with_obstacles,
    minimum_path_sum,
    climbing_stairs,
    decode_ways_dp,
    word_break_dp,
    partition_equal_subset_sum,
)


class TestCoinChange:
    """Test coin_change function."""

    def test_simple_case(self):
        assert coin_change([1, 3, 4], 6) == 2

    def test_impossible_case(self):
        assert coin_change([2], 3) == -1

    def test_zero_amount(self):
        assert coin_change([1], 0) == 0

    def test_single_coin_exact(self):
        assert coin_change([5], 5) == 1

    def test_greedy_fails(self):
        # Greedy would choose [4, 1] but optimal is [3, 3]
        assert coin_change([1, 3, 4], 6) == 2

    def test_large_amount(self):
        result = coin_change([1, 2, 5], 11)
        assert result == 3  # 5 + 5 + 1


class TestCoinChangeCombinations:
    """Test coin_change_combinations function."""

    def test_simple_case(self):
        assert coin_change_combinations([1, 2, 5], 5) == 4

    def test_impossible_case(self):
        assert coin_change_combinations([2], 3) == 0

    def test_exact_match(self):
        assert coin_change_combinations([10], 10) == 1

    def test_zero_amount(self):
        assert coin_change_combinations([1, 2, 5], 0) == 1

    def test_single_coin(self):
        assert coin_change_combinations([1], 5) == 1


class TestLongestIncreasingSubsequence:
    """Test longest_increasing_subsequence function."""

    def test_complex_case(self):
        assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4

    def test_another_case(self):
        assert longest_increasing_subsequence([0, 1, 0, 3, 2, 3]) == 4

    def test_all_same(self):
        assert longest_increasing_subsequence([7, 7, 7, 7, 7, 7, 7]) == 1

    def test_strictly_increasing(self):
        assert longest_increasing_subsequence([1, 2, 3, 4, 5]) == 5

    def test_strictly_decreasing(self):
        assert longest_increasing_subsequence([5, 4, 3, 2, 1]) == 1

    def test_single_element(self):
        assert longest_increasing_subsequence([1]) == 1

    def test_empty_array(self):
        assert longest_increasing_subsequence([]) == 0


class TestLongestIncreasingSubsequenceSequence:
    """Test longest_increasing_subsequence_sequence function."""

    def test_simple_case(self):
        result = longest_increasing_subsequence_sequence([10, 9, 2, 5, 3, 7, 101, 18])
        assert len(result) == 4
        assert result == sorted(result)  # Should be increasing

    def test_single_element(self):
        result = longest_increasing_subsequence_sequence([5])
        assert result == [5]

    def test_strictly_increasing(self):
        result = longest_increasing_subsequence_sequence([1, 2, 3, 4])
        assert result == [1, 2, 3, 4]


class TestMaximumProductSubarray:
    """Test maximum_product_subarray function."""

    def test_simple_case(self):
        assert maximum_product_subarray([2, 3, -2, 4]) == 6

    def test_with_zero(self):
        assert maximum_product_subarray([-2, 0, -1]) == 0

    def test_negative_numbers(self):
        assert maximum_product_subarray([-2, 3, -4]) == 24

    def test_single_element(self):
        assert maximum_product_subarray([5]) == 5
        assert maximum_product_subarray([-5]) == -5

    def test_all_negative(self):
        assert maximum_product_subarray([-1, -2, -3]) == 6


class TestHouseRobber:
    """Test house_robber function."""

    def test_simple_case(self):
        assert house_robber([1, 2, 3, 1]) == 4

    def test_complex_case(self):
        assert house_robber([2, 7, 9, 3, 1]) == 12

    def test_single_house(self):
        assert house_robber([5]) == 5

    def test_two_houses(self):
        assert house_robber([1, 2]) == 2
        assert house_robber([2, 1]) == 2

    def test_empty_houses(self):
        assert house_robber([]) == 0


class TestHouseRobberCircular:
    """Test house_robber_circular function."""

    def test_simple_case(self):
        assert house_robber_circular([2, 3, 2]) == 3

    def test_four_houses(self):
        assert house_robber_circular([1, 2, 3, 1]) == 4

    def test_three_houses(self):
        assert house_robber_circular([1, 2, 3]) == 3

    def test_single_house(self):
        assert house_robber_circular([5]) == 5

    def test_two_houses(self):
        assert house_robber_circular([1, 2]) == 2


class TestJumpGame:
    """Test jump_game function."""

    def test_can_reach(self):
        assert jump_game([2, 3, 1, 1, 4])

    def test_cannot_reach(self):
        assert not jump_game([3, 2, 1, 0, 4])

    def test_single_element(self):
        assert jump_game([0])

    def test_immediate_reach(self):
        assert jump_game([1])

    def test_large_first_jump(self):
        assert jump_game([5, 1, 1, 1, 1])

    def test_stuck_at_zero(self):
        assert not jump_game([1, 0, 1, 0])


class TestJumpGameMinJumps:
    """Test jump_game_min_jumps function."""

    def test_simple_case(self):
        assert jump_game_min_jumps([2, 3, 1, 1, 4]) == 2

    def test_another_case(self):
        assert jump_game_min_jumps([2, 3, 0, 1, 4]) == 2

    def test_all_ones(self):
        assert jump_game_min_jumps([1, 1, 1, 1]) == 3

    def test_single_element(self):
        assert jump_game_min_jumps([0]) == 0

    def test_large_first_jump(self):
        assert jump_game_min_jumps([5]) == 0


class TestUniquePathsGrid:
    """Test unique_paths_grid function."""

    def test_simple_case(self):
        assert unique_paths_grid(3, 7) == 28

    def test_small_grid(self):
        assert unique_paths_grid(3, 2) == 3

    def test_single_cell(self):
        assert unique_paths_grid(1, 1) == 1

    def test_single_row(self):
        assert unique_paths_grid(1, 5) == 1

    def test_single_column(self):
        assert unique_paths_grid(5, 1) == 1

    def test_square_grid(self):
        assert unique_paths_grid(3, 3) == 6


class TestUniquePathsWithObstacles:
    """Test unique_paths_with_obstacles function."""

    def test_simple_case(self):
        grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        assert unique_paths_with_obstacles(grid) == 2

    def test_blocked_start(self):
        grid = [[1, 0], [0, 0]]
        assert unique_paths_with_obstacles(grid) == 0

    def test_blocked_end(self):
        grid = [[0, 0], [0, 1]]
        assert unique_paths_with_obstacles(grid) == 0

    def test_no_obstacles(self):
        grid = [[0, 0], [0, 0]]
        assert unique_paths_with_obstacles(grid) == 2

    def test_single_cell_free(self):
        grid = [[0]]
        assert unique_paths_with_obstacles(grid) == 1

    def test_single_cell_blocked(self):
        grid = [[1]]
        assert unique_paths_with_obstacles(grid) == 0


class TestMinimumPathSum:
    """Test minimum_path_sum function."""

    def test_simple_case(self):
        grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
        assert minimum_path_sum(grid) == 7

    def test_another_case(self):
        grid = [[1, 2, 3], [4, 5, 6]]
        assert minimum_path_sum(grid) == 12

    def test_single_cell(self):
        grid = [[5]]
        assert minimum_path_sum(grid) == 5

    def test_single_row(self):
        grid = [[1, 2, 3, 4]]
        assert minimum_path_sum(grid) == 10

    def test_single_column(self):
        grid = [[1], [2], [3], [4]]
        assert minimum_path_sum(grid) == 10


class TestClimbingStairs:
    """Test climbing_stairs function."""

    def test_small_cases(self):
        assert climbing_stairs(2) == 2
        assert climbing_stairs(3) == 3
        assert climbing_stairs(4) == 5

    def test_base_cases(self):
        assert climbing_stairs(1) == 1
        assert climbing_stairs(0) == 1

    def test_larger_case(self):
        assert climbing_stairs(5) == 8
        assert climbing_stairs(6) == 13


class TestDecodeWaysDP:
    """Test decode_ways_dp function."""

    def test_simple_cases(self):
        assert decode_ways_dp("12") == 2
        assert decode_ways_dp("226") == 3

    def test_invalid_cases(self):
        assert decode_ways_dp("0") == 0
        assert decode_ways_dp("06") == 0

    def test_valid_cases(self):
        assert decode_ways_dp("10") == 1
        assert decode_ways_dp("27") == 1

    def test_single_digit(self):
        assert decode_ways_dp("1") == 1
        assert decode_ways_dp("9") == 1


class TestWordBreakDP:
    """Test word_break_dp function."""

    def test_valid_break(self):
        assert word_break_dp("leetcode", ["leet", "code"])

    def test_another_valid_break(self):
        assert word_break_dp("applepenapple", ["apple", "pen"])

    def test_invalid_break(self):
        assert not word_break_dp("catsandog", ["cats", "dog", "sand", "and", "cat"])

    def test_empty_string(self):
        assert word_break_dp("", ["a", "b"])

    def test_repeated_usage(self):
        assert word_break_dp("aaaaaaa", ["aaaa", "aaa"])


class TestPartitionEqualSubsetSum:
    """Test partition_equal_subset_sum function."""

    def test_valid_partition(self):
        assert partition_equal_subset_sum([1, 5, 11, 5])

    def test_invalid_partition(self):
        assert not partition_equal_subset_sum([1, 2, 3, 5])

    def test_another_invalid(self):
        assert not partition_equal_subset_sum([1, 2, 5])

    def test_single_element(self):
        assert not partition_equal_subset_sum([1])

    def test_two_equal_elements(self):
        assert partition_equal_subset_sum([1, 1])

    def test_odd_sum(self):
        assert not partition_equal_subset_sum([1, 3, 5])

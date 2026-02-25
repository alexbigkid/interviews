"""Tests for advanced array algorithms."""

from src.array.advanced_algorithms import (
    merge_intervals,
    insert_interval,
    non_overlapping_intervals,
    meeting_rooms_ii,
    spiral_matrix,
    generate_spiral_matrix,
    rotate_matrix_90,
    set_matrix_zeros,
    search_2d_matrix,
    search_2d_matrix_ii,
    find_peak_element,
    first_missing_positive,
    trapping_rain_water,
    candy_distribution,
    gas_station_circuit,
    h_index,
)


class TestMergeIntervals:
    """Test merge_intervals function."""

    def test_simple_case(self):
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
        result = merge_intervals(intervals)
        expected = [[1, 6], [8, 10], [15, 18]]
        assert result == expected

    def test_touching_intervals(self):
        intervals = [[1, 4], [4, 5]]
        result = merge_intervals(intervals)
        assert result == [[1, 5]]

    def test_overlapping_intervals(self):
        intervals = [[1, 4], [0, 4]]
        result = merge_intervals(intervals)
        assert result == [[0, 4]]

    def test_no_overlap(self):
        intervals = [[1, 2], [3, 4], [5, 6]]
        result = merge_intervals(intervals)
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_single_interval(self):
        intervals = [[1, 4]]
        result = merge_intervals(intervals)
        assert result == [[1, 4]]


class TestInsertInterval:
    """Test insert_interval function."""

    def test_simple_insert(self):
        intervals = [[1, 3], [6, 9]]
        new_interval = [2, 5]
        result = insert_interval(intervals, new_interval)
        expected = [[1, 5], [6, 9]]
        assert result == expected

    def test_merge_multiple(self):
        intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
        new_interval = [4, 8]
        result = insert_interval(intervals, new_interval)
        expected = [[1, 2], [3, 10], [12, 16]]
        assert result == expected

    def test_insert_at_beginning(self):
        intervals = [[3, 4], [5, 6]]
        new_interval = [1, 2]
        result = insert_interval(intervals, new_interval)
        expected = [[1, 2], [3, 4], [5, 6]]
        assert result == expected

    def test_insert_at_end(self):
        intervals = [[1, 2], [3, 4]]
        new_interval = [5, 6]
        result = insert_interval(intervals, new_interval)
        expected = [[1, 2], [3, 4], [5, 6]]
        assert result == expected


class TestNonOverlappingIntervals:
    """Test non_overlapping_intervals function."""

    def test_simple_case(self):
        intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
        assert non_overlapping_intervals(intervals) == 1

    def test_many_overlaps(self):
        intervals = [[1, 2], [1, 2], [1, 2]]
        assert non_overlapping_intervals(intervals) == 2

    def test_no_overlaps(self):
        intervals = [[1, 2], [2, 3]]
        assert non_overlapping_intervals(intervals) == 0

    def test_single_interval(self):
        intervals = [[1, 2]]
        assert non_overlapping_intervals(intervals) == 0


class TestMeetingRoomsII:
    """Test meeting_rooms_ii function."""

    def test_simple_case(self):
        intervals = [[0, 30], [5, 10], [15, 20]]
        assert meeting_rooms_ii(intervals) == 2

    def test_no_overlap(self):
        intervals = [[7, 10], [2, 4]]
        assert meeting_rooms_ii(intervals) == 1

    def test_many_overlaps(self):
        intervals = [[9, 10], [4, 9], [4, 17]]
        assert meeting_rooms_ii(intervals) == 2

    def test_single_meeting(self):
        intervals = [[1, 5]]
        assert meeting_rooms_ii(intervals) == 1

    def test_empty_meetings(self):
        intervals = []
        assert meeting_rooms_ii(intervals) == 0


class TestSpiralMatrix:
    """Test spiral_matrix function."""

    def test_3x3_matrix(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = spiral_matrix(matrix)
        expected = [1, 2, 3, 6, 9, 8, 7, 4, 5]
        assert result == expected

    def test_3x4_matrix(self):
        matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        result = spiral_matrix(matrix)
        expected = [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
        assert result == expected

    def test_single_row(self):
        matrix = [[1, 2, 3]]
        result = spiral_matrix(matrix)
        assert result == [1, 2, 3]

    def test_single_column(self):
        matrix = [[1], [2], [3]]
        result = spiral_matrix(matrix)
        assert result == [1, 2, 3]

    def test_single_element(self):
        matrix = [[1]]
        result = spiral_matrix(matrix)
        assert result == [1]


class TestGenerateSpiralMatrix:
    """Test generate_spiral_matrix function."""

    def test_3x3_generation(self):
        result = generate_spiral_matrix(3)
        expected = [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
        assert result == expected

    def test_1x1_generation(self):
        result = generate_spiral_matrix(1)
        assert result == [[1]]

    def test_2x2_generation(self):
        result = generate_spiral_matrix(2)
        expected = [[1, 2], [4, 3]]
        assert result == expected

    def test_4x4_generation(self):
        result = generate_spiral_matrix(4)
        assert len(result) == 4
        assert len(result[0]) == 4
        assert result[0][0] == 1
        assert result[0][-1] == 4


class TestRotateMatrix90:
    """Test rotate_matrix_90 function."""

    def test_3x3_rotation(self):
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        rotate_matrix_90(matrix)
        expected = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
        assert matrix == expected

    def test_4x4_rotation(self):
        matrix = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
        rotate_matrix_90(matrix)
        expected = [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]
        assert matrix == expected

    def test_1x1_rotation(self):
        matrix = [[1]]
        rotate_matrix_90(matrix)
        assert matrix == [[1]]

    def test_2x2_rotation(self):
        matrix = [[1, 2], [3, 4]]
        rotate_matrix_90(matrix)
        expected = [[3, 1], [4, 2]]
        assert matrix == expected


class TestSetMatrixZeros:
    """Test set_matrix_zeros function."""

    def test_simple_case(self):
        matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        set_matrix_zeros(matrix)
        expected = [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
        assert matrix == expected

    def test_multiple_zeros(self):
        matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
        set_matrix_zeros(matrix)
        expected = [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
        assert matrix == expected

    def test_no_zeros(self):
        matrix = [[1, 2, 3], [4, 5, 6]]
        original = [row[:] for row in matrix]  # Deep copy
        set_matrix_zeros(matrix)
        assert matrix == original

    def test_all_zeros(self):
        matrix = [[0, 0], [0, 0]]
        set_matrix_zeros(matrix)
        assert matrix == [[0, 0], [0, 0]]


class TestSearch2DMatrix:
    """Test search_2d_matrix function."""

    def test_target_found(self):
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        assert search_2d_matrix(matrix, 3)

    def test_target_not_found(self):
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        assert not search_2d_matrix(matrix, 13)

    def test_first_element(self):
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        assert search_2d_matrix(matrix, 1)

    def test_last_element(self):
        matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        assert search_2d_matrix(matrix, 60)

    def test_single_element(self):
        matrix = [[1]]
        assert search_2d_matrix(matrix, 1)
        assert not search_2d_matrix(matrix, 2)


class TestSearch2DMatrixII:
    """Test search_2d_matrix_ii function."""

    def test_target_found(self):
        matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
        assert search_2d_matrix_ii(matrix, 5)

    def test_target_not_found(self):
        matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
        assert not search_2d_matrix_ii(matrix, 20)

    def test_corner_elements(self):
        matrix = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22], [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
        assert search_2d_matrix_ii(matrix, 1)  # Top-left
        assert search_2d_matrix_ii(matrix, 30)  # Bottom-right
        assert search_2d_matrix_ii(matrix, 15)  # Top-right
        assert search_2d_matrix_ii(matrix, 18)  # Bottom-left


class TestFindPeakElement:
    """Test find_peak_element function."""

    def test_simple_peak(self):
        result = find_peak_element([1, 2, 3, 1])
        assert result == 2

    def test_multiple_peaks(self):
        result = find_peak_element([1, 2, 1, 3, 5, 6, 4])
        assert result in [1, 5]  # Both are valid peaks

    def test_single_element(self):
        result = find_peak_element([1])
        assert result == 0

    def test_increasing_sequence(self):
        result = find_peak_element([1, 2, 3, 4, 5])
        assert result == 4

    def test_decreasing_sequence(self):
        result = find_peak_element([5, 4, 3, 2, 1])
        assert result == 0


class TestFirstMissingPositive:
    """Test first_missing_positive function."""

    def test_simple_case(self):
        assert first_missing_positive([1, 2, 0]) == 3

    def test_missing_one(self):
        assert first_missing_positive([3, 4, -1, 1]) == 2

    def test_large_numbers(self):
        assert first_missing_positive([7, 8, 9, 11, 12]) == 1

    def test_consecutive_sequence(self):
        assert first_missing_positive([1, 2, 3, 4]) == 5

    def test_single_element(self):
        assert first_missing_positive([1]) == 2
        assert first_missing_positive([0]) == 1

    def test_negative_numbers(self):
        assert first_missing_positive([-1, -2, -3]) == 1


class TestTrappingRainWater:
    """Test trapping_rain_water function."""

    def test_simple_case(self):
        assert trapping_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    def test_another_case(self):
        assert trapping_rain_water([4, 2, 0, 3, 2, 5]) == 9

    def test_no_water_trapped(self):
        assert trapping_rain_water([1, 2, 3, 4, 5]) == 0
        assert trapping_rain_water([5, 4, 3, 2, 1]) == 0

    def test_single_valley(self):
        assert trapping_rain_water([3, 0, 2]) == 2

    def test_flat_areas(self):
        assert trapping_rain_water([3, 3, 3]) == 0


class TestCandyDistribution:
    """Test candy_distribution function."""

    def test_simple_case(self):
        assert candy_distribution([1, 0, 2]) == 5

    def test_equal_ratings(self):
        assert candy_distribution([1, 2, 2]) == 4

    def test_complex_case(self):
        assert candy_distribution([1, 3, 2, 2, 1]) == 7

    def test_single_child(self):
        assert candy_distribution([1]) == 1

    def test_increasing_ratings(self):
        assert candy_distribution([1, 2, 3, 4]) == 10

    def test_decreasing_ratings(self):
        assert candy_distribution([4, 3, 2, 1]) == 10


class TestGasStationCircuit:
    """Test gas_station_circuit function."""

    def test_valid_circuit(self):
        gas = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
        assert gas_station_circuit(gas, cost) == 3

    def test_impossible_circuit(self):
        gas = [2, 3, 4]
        cost = [3, 4, 3]
        assert gas_station_circuit(gas, cost) == -1

    def test_single_station(self):
        gas = [5]
        cost = [4]
        assert gas_station_circuit(gas, cost) == 0

    def test_exact_gas_needed(self):
        gas = [3, 1, 1]
        cost = [1, 2, 2]
        result = gas_station_circuit(gas, cost)
        assert result >= 0


class TestHIndex:
    """Test h_index function."""

    def test_simple_case(self):
        assert h_index([3, 0, 6, 1, 5]) == 3

    def test_another_case(self):
        assert h_index([1, 3, 1]) == 1

    def test_single_paper(self):
        assert h_index([100]) == 1

    def test_no_citations(self):
        assert h_index([0, 0, 0]) == 0

    def test_high_citations(self):
        assert h_index([10, 8, 5, 4, 3]) == 4

    def test_equal_citations(self):
        assert h_index([5, 5, 5, 5, 5]) == 5

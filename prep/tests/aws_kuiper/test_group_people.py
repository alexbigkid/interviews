"""Tests for group people functionality."""

import pytest
from src.aws_kuiper.group_people import group_people


class TestGroupPeople:
    """Test group_people function."""

    @pytest.mark.parametrize(
        "group_sizes,expected",
        [
            # Example 1: Mixed group sizes
            ([2, 1, 3, 3, 3, 2], [[1], [0, 5], [2, 3, 4]]),
            # Example 2: From problem description
            ([3, 3, 3, 3, 3, 1, 3], [[5], [0, 1, 2], [3, 4, 6]]),
            # Single person
            ([1], [[0]]),
            # All same size groups
            ([2, 2, 2, 2], [[0, 1], [2, 3]]),
            # Large group
            ([5, 5, 5, 5, 5], [[0, 1, 2, 3, 4]]),
            # Multiple groups of size 1
            ([1, 1, 1], [[0], [1], [2]]),
            # Mix of sizes requiring multiple groups
            ([2, 2, 2, 2, 3, 3, 3], [[0, 1], [2, 3], [4, 5, 6]]),
        ],
    )
    def test_group_people_valid_cases(self, group_sizes, expected):
        """Test group_people with valid inputs using parametrized test cases."""
        result = group_people(group_sizes)

        # Since order doesn't matter, we need to validate the result differently
        self._validate_grouping(group_sizes, result, expected)

    def _validate_grouping(self, group_sizes, result, expected):
        """Helper method to validate the grouping result."""
        # Check that all people are included exactly once
        all_people_result = sorted([person for group in result for person in group])
        all_people_expected = list(range(len(group_sizes)))
        assert all_people_result == all_people_expected, "All people should be included exactly once"

        # Check that each group has the correct size
        for group in result:
            if group:  # Non-empty group
                group_size = len(group)
                for person in group:
                    msg = f"Person {person} requires group size {group_sizes[person]} but is in group of size {group_size}"
                    assert group_sizes[person] == group_size, msg

        # Check that we have the same number of groups (order-independent)
        assert len(result) == len(expected), "Number of groups should match"

        # Sort both results for comparison (since order doesn't matter)
        result_sorted = sorted([sorted(group) for group in result])
        expected_sorted = sorted([sorted(group) for group in expected])
        assert result_sorted == expected_sorted, "Groups should match expected result"

    @pytest.mark.parametrize(
        "group_sizes",
        [
            # Edge case: minimum input
            [1],
            # All people need to be in one large group
            [6, 6, 6, 6, 6, 6],
            # Complex mix
            [4, 4, 4, 4, 2, 2, 1, 1, 1],
        ],
    )
    def test_group_people_properties(self, group_sizes):
        """Test that group_people satisfies required properties without checking exact output."""
        result = group_people(group_sizes)

        # All people should be included exactly once
        all_people = []
        for group in result:
            all_people.extend(group)

        assert sorted(all_people) == list(range(len(group_sizes))), "All people should be included exactly once"

        # Each group should have the correct size for all its members
        for group in result:
            if group:  # Non-empty group
                expected_size = len(group)
                for person in group:
                    msg = f"Person {person} should be in group of size {group_sizes[person]}, not {expected_size}"
                    assert group_sizes[person] == expected_size, msg

    def test_empty_input(self):
        """Test with empty input."""
        result = group_people([])
        assert result == [], "Empty input should return empty result"

    def test_single_large_group(self):
        """Test case where everyone goes in one group."""
        group_sizes = [4, 4, 4, 4]
        result = group_people(group_sizes)
        assert len(result) == 1, "Should have exactly one group"
        assert sorted(result[0]) == [0, 1, 2, 3], "All people should be in the single group"

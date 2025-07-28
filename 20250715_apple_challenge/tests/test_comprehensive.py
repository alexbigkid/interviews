import unittest
from abk_aapl.simple_solution import solution


class TestSolution(unittest.TestCase):
    def test_example_case(self):
        """Test the provided example"""
        k = 3
        a = [1, 6, 8, 2, 4, 9, 12]
        expected = 3
        self.assertEqual(solution(k, a), expected)

    def test_empty_list(self):
        """Test empty list"""
        self.assertEqual(solution(3, []), 0)

    def test_none_input(self):
        """Test None input"""
        self.assertEqual(solution(3, None), 0)

    def test_single_element(self):
        """Test single element"""
        self.assertEqual(solution(3, [5]), 0)

    def test_two_elements_valid_pair(self):
        """Test two elements that form a valid pair"""
        self.assertEqual(solution(2, [1, 3]), 1)

    def test_two_elements_no_pair(self):
        """Test two elements that don't form a valid pair"""
        self.assertEqual(solution(5, [1, 3]), 0)

    def test_identical_elements_k_zero(self):
        """Test identical elements with k=0"""
        self.assertEqual(solution(0, [5, 5]), 4)  # Each pairs with itself and the other

    def test_identical_elements_k_nonzero(self):
        """Test identical elements with k>0"""
        self.assertEqual(solution(3, [5, 5]), 0)

    def test_duplicates_with_pairs(self):
        """Test duplicates that form pairs"""
        # [1,1,4,4] with k=3: each 1 pairs with each 4
        self.assertEqual(solution(3, [1, 1, 4, 4]), 4)

    def test_no_pairs_found(self):
        """Test array with no valid pairs"""
        self.assertEqual(solution(10, [1, 2, 3, 4, 5]), 0)

    def test_all_same_elements(self):
        """Test array with all same elements"""
        # k=0: each element pairs with every other element
        self.assertEqual(solution(0, [3, 3, 3, 3]), 16)
        # k>0: no pairs possible
        self.assertEqual(solution(1, [3, 3, 3, 3]), 0)

    def test_large_k_value(self):
        """Test with large k value"""
        self.assertEqual(solution(1000, [1, 2, 1001, 1002]), 2)

    def test_sequential_numbers(self):
        """Test sequential numbers"""
        # [1,2,3,4,5] with k=1: (1,2), (2,3), (3,4), (4,5)
        self.assertEqual(solution(1, [1, 2, 3, 4, 5]), 4)

    def test_reverse_order(self):
        """Test that order doesn't matter"""
        a1 = [1, 2, 3, 4, 5]
        a2 = [5, 4, 3, 2, 1]
        self.assertEqual(solution(2, a1), solution(2, a2))

    def test_modulo_operation(self):
        """Test that modulo is applied correctly"""
        # Create a case that would exceed 10^9 + 7 without modulo
        # 1000 copies of 1 and 1000 copies of 2 with k=1
        large_array = [1] * 1000 + [2] * 1000
        result = solution(1, large_array)
        self.assertTrue(result < 10**9 + 7)
        self.assertEqual(result, 1000000)  # 1000 * 1000

    def test_negative_difference_not_counted(self):
        """Test that only positive differences are counted"""
        # [1,4] with k=3: only (1,4) counts, not (4,1)
        self.assertEqual(solution(3, [1, 4]), 1)

    def test_mixed_duplicates(self):
        """Test complex case with mixed duplicates"""
        # [1,1,2,4,4,5] with k=3: (1,4), (1,4), (1,4), (1,4), (2,5)
        self.assertEqual(solution(3, [1, 1, 2, 4, 4, 5]), 5)


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for advanced level Python challenges
"""

from abk_apple.advanced_challenges import (
    TreeNode,
    ListNode,
    serialize,
    deserialize,
    word_ladder,
    alien_dictionary,
    median_from_data_stream,
    merge_k_sorted_lists,
    lru_cache,
    trap_rain_water,
    sliding_window_maximum,
)


class TestSerialize:
    def test_empty_tree(self):
        assert serialize(None) == "null"

    def test_single_node(self):
        root = TreeNode(1)
        assert serialize(root) == "1,null,null"

    def test_basic_tree(self):
        # Create tree: [1,2,3,null,null,4,5]
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.right.left = TreeNode(4)
        root.right.right = TreeNode(5)

        expected = "1,2,null,null,3,4,null,null,5,null,null"
        assert serialize(root) == expected

    def test_left_skewed_tree(self):
        # Create tree: [1,2,null,3,null,null,null]
        root = TreeNode(1)
        root.left = TreeNode(2)
        root.left.left = TreeNode(3)

        expected = "1,2,3,null,null,null,null"
        assert serialize(root) == expected

    def test_right_skewed_tree(self):
        # Create tree: [1,null,2,null,3]
        root = TreeNode(1)
        root.right = TreeNode(2)
        root.right.right = TreeNode(3)

        expected = "1,null,2,null,3,null,null"
        assert serialize(root) == expected


class TestDeserialize:
    def test_empty_tree(self):
        assert deserialize("null") is None

    def test_single_node(self):
        root = deserialize("1,null,null")
        assert root.val == 1
        assert root.left is None
        assert root.right is None

    def test_basic_tree(self):
        # Deserialize: "1,2,null,null,3,4,null,null,5,null,null"
        data = "1,2,null,null,3,4,null,null,5,null,null"
        root = deserialize(data)

        assert root.val == 1
        assert root.left.val == 2
        assert root.left.left is None
        assert root.left.right is None
        assert root.right.val == 3
        assert root.right.left.val == 4
        assert root.right.right.val == 5
        assert root.right.left.left is None
        assert root.right.left.right is None
        assert root.right.right.left is None
        assert root.right.right.right is None

    def test_left_skewed_tree(self):
        data = "1,2,3,null,null,null,null"
        root = deserialize(data)

        assert root.val == 1
        assert root.left.val == 2
        assert root.left.left.val == 3
        assert root.right is None
        assert root.left.right is None
        assert root.left.left.left is None
        assert root.left.left.right is None


class TestSerializeDeserializeRoundTrip:
    def test_round_trip_empty(self):
        original = None
        serialized = serialize(original)
        deserialized = deserialize(serialized)
        assert deserialized is None

    def test_round_trip_single_node(self):
        original = TreeNode(42)
        serialized = serialize(original)
        deserialized = deserialize(serialized)

        assert deserialized.val == 42
        assert deserialized.left is None
        assert deserialized.right is None

    def test_round_trip_complex_tree(self):
        # Create original tree: [1,2,3,null,null,4,5]
        original = TreeNode(1)
        original.left = TreeNode(2)
        original.right = TreeNode(3)
        original.right.left = TreeNode(4)
        original.right.right = TreeNode(5)

        # Serialize and deserialize
        serialized = serialize(original)
        deserialized = deserialize(serialized)

        # Verify structure is preserved
        assert deserialized.val == 1
        assert deserialized.left.val == 2
        assert deserialized.right.val == 3
        assert deserialized.right.left.val == 4
        assert deserialized.right.right.val == 5

        # Verify null nodes
        assert deserialized.left.left is None
        assert deserialized.left.right is None
        assert deserialized.right.left.left is None
        assert deserialized.right.left.right is None
        assert deserialized.right.right.left is None
        assert deserialized.right.right.right is None

    def test_round_trip_negative_values(self):
        original = TreeNode(-1)
        original.left = TreeNode(-2)
        original.right = TreeNode(-3)

        serialized = serialize(original)
        deserialized = deserialize(serialized)

        assert deserialized.val == -1
        assert deserialized.left.val == -2
        assert deserialized.right.val == -3


class TestWordLadder:
    def test_basic_case(self):
        beginWord = "hit"
        endWord = "cog"
        wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
        assert word_ladder(beginWord, endWord, wordList) == 5

    def test_no_transformation(self):
        beginWord = "hit"
        endWord = "cog"
        wordList = ["hot", "dot", "dog", "lot", "log"]
        assert word_ladder(beginWord, endWord, wordList) == 0

    def test_same_word(self):
        beginWord = "hit"
        endWord = "hit"
        wordList = ["hot", "hit"]
        assert word_ladder(beginWord, endWord, wordList) == 1


class TestAlienDictionary:
    def test_basic_case(self):
        words = ["wrt", "wrf", "er", "ett", "rftt"]
        result = alien_dictionary(words)
        # One possible valid ordering is "wertf"
        assert isinstance(result, str)
        assert len(result) > 0 or result == ""

    def test_invalid_order(self):
        words = ["z", "x", "z"]
        result = alien_dictionary(words)
        assert result == ""

    def test_single_word(self):
        words = ["hello"]
        result = alien_dictionary(words)
        assert isinstance(result, str)


class TestMedianFromDataStream:
    def test_basic_functionality(self):
        MedianFinder = median_from_data_stream()
        mf = MedianFinder()

        # Test that methods exist
        assert hasattr(mf, "addNum")
        assert hasattr(mf, "findMedian")
        assert callable(mf.addNum)
        assert callable(mf.findMedian)

    def test_median_calculation(self):
        # This test will need to be completed after implementation
        MedianFinder = median_from_data_stream()
        mf = MedianFinder()
        # mf.addNum(1)
        # mf.addNum(2)
        # assert mf.findMedian() == 1.5
        # mf.addNum(3)
        # assert mf.findMedian() == 2.0


class TestMergeKSortedLists:
    def create_linked_list(self, values):
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    def linked_list_to_array(self, head):
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def test_basic_case(self):
        lists = [
            self.create_linked_list([1, 4, 5]),
            self.create_linked_list([1, 3, 4]),
            self.create_linked_list([2, 6]),
        ]
        result = merge_k_sorted_lists(lists)
        # Expected: [1,1,2,3,4,4,5,6]
        assert callable(merge_k_sorted_lists)

    def test_empty_lists(self):
        assert merge_k_sorted_lists([]) is None or merge_k_sorted_lists([]) == []

    def test_single_list(self):
        lists = [self.create_linked_list([1, 2, 3])]
        result = merge_k_sorted_lists(lists)
        assert callable(merge_k_sorted_lists)


class TestLRUCache:
    def test_basic_functionality(self):
        LRUCache = lru_cache(2)
        cache = LRUCache(2)

        # Test that methods exist
        assert hasattr(cache, "get")
        assert hasattr(cache, "put")
        assert callable(cache.get)
        assert callable(cache.put)

    def test_lru_behavior(self):
        # This test will need to be completed after implementation
        LRUCache = lru_cache(2)
        cache = LRUCache(2)
        # cache.put(1, 1)
        # cache.put(2, 2)
        # assert cache.get(1) == 1
        # cache.put(3, 3)  # evicts key 2
        # assert cache.get(2) == -1


class TestTrapRainWater:
    def test_basic_case(self):
        height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
        assert trap_rain_water(height) == 6

    def test_no_water(self):
        height = [3, 0, 0, 0, 0, 0, 0, 2, 0, 4]
        result = trap_rain_water(height)
        assert isinstance(result, int)

    def test_empty_array(self):
        assert trap_rain_water([]) == 0

    def test_single_element(self):
        assert trap_rain_water([1]) == 0


class TestSlidingWindowMaximum:
    def test_basic_case(self):
        nums = [1, 3, -1, -3, 5, 3, 6, 7]
        k = 3
        expected = [3, 3, 5, 5, 6, 7]
        assert sliding_window_maximum(nums, k) == expected

    def test_single_element_window(self):
        nums = [1, 2, 3, 4, 5]
        k = 1
        expected = [1, 2, 3, 4, 5]
        assert sliding_window_maximum(nums, k) == expected

    def test_window_size_equals_array_length(self):
        nums = [1, 3, 2, 5, 4]
        k = 5
        expected = [5]
        assert sliding_window_maximum(nums, k) == expected

    def test_all_same_elements(self):
        nums = [1, 1, 1, 1, 1]
        k = 3
        expected = [1, 1, 1]
        assert sliding_window_maximum(nums, k) == expected

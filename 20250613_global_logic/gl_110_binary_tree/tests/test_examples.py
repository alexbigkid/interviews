"""Tests for binary tree examples module."""

from binary_tree_prep.examples import main
from binary_tree_prep.binary_tree import BinaryTree, TreeNode


class TestExamples:
    """Test the examples module."""

    def test_main_runs_without_error(self, capsys):
        """Test that the main function runs without throwing any errors."""
        main()
        captured = capsys.readouterr()
        assert "Binary Tree Interview Preparation Examples" in captured.out
        assert len(captured.out) > 0

    def test_example_tree_creation(self):
        """Test the tree creation examples work correctly."""
        tree1 = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
        expected_levels = [[3], [9, 20], [15, 7]]
        assert tree1.level_order_traversal() == expected_levels

        root = TreeNode(1)
        root.left = TreeNode(2)
        root.right = TreeNode(3)
        root.left.left = TreeNode(4)
        root.left.right = TreeNode(5)
        tree2 = BinaryTree(root)
        expected_manual = [[1], [2, 3], [4, 5]]
        assert tree2.level_order_traversal() == expected_manual

    def test_dfs_traversal_examples(self):
        """Test that DFS traversal examples produce correct results."""
        tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])

        assert tree.inorder_traversal() == [4, 2, 5, 1, 6, 3, 7]
        assert tree.preorder_traversal() == [1, 2, 4, 5, 3, 6, 7]
        assert tree.postorder_traversal() == [4, 5, 2, 6, 7, 3, 1]

    def test_bfs_traversal_example(self):
        """Test that BFS traversal example produces correct results."""
        tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
        levels = tree.level_order_traversal()
        expected = [[3], [9, 20], [15, 7]]
        assert levels == expected

    def test_tree_properties_example(self):
        """Test that tree properties example calculations are correct."""
        tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])

        assert tree.max_depth() == 3
        assert tree.min_depth() == 2
        assert tree.diameter() == 3
        assert tree.is_balanced() is True

    def test_path_sum_example(self):
        """Test that path sum example works correctly."""
        tree = BinaryTree.from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
        target = 22
        assert tree.path_sum_exists(target) is True

    def test_tree_views_example(self):
        """Test that tree views example produces correct results."""
        tree = BinaryTree.from_list([1, 2, 3, None, 5, None, 4])
        right_view = tree.right_side_view()
        expected = [1, 3, 4]
        assert right_view == expected

    def test_lca_example(self):
        """Test that LCA example works correctly."""
        tree = BinaryTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])

        def find_node(root, val):
            if not root:
                return None
            if root.val == val:
                return root
            return find_node(root.left, val) or find_node(root.right, val)

        node5 = find_node(tree.root, 5)
        node1 = find_node(tree.root, 1)
        lca = tree.lowest_common_ancestor(node5, node1)
        assert lca.val == 3

    def test_serialization_example(self):
        """Test that serialization example works correctly."""
        tree = BinaryTree.from_list([1, 2, 3, None, None, 4, 5])
        original_levels = tree.level_order_traversal()

        serialized = tree.serialize()
        deserialized_tree = BinaryTree.deserialize(serialized)
        deserialized_levels = deserialized_tree.level_order_traversal()

        assert original_levels == deserialized_levels

    def test_interview_scenarios(self):
        """Test various interview scenarios mentioned in examples."""
        scenarios = [
            ("Complete Binary Tree", [1, 2, 3, 4, 5, 6, 7]),
            ("Perfect Binary Tree", [1, 2, 3, 4, 5, 6, 7]),
            ("Balanced Binary Tree", [1, 2, 3, 4, 5, 6]),
            ("Unbalanced Binary Tree", [1, 2, None, 3, None, 4]),
            ("Left Skewed Tree", [1, 2, None, 3, None, 4]),
            ("Right Skewed Tree", [1, None, 2, None, None, None, 3]),
            ("Single Node", [1]),
        ]

        for _, values in scenarios:
            if values:
                tree = BinaryTree.from_list(values)
                levels = tree.level_order_traversal()
                depth = tree.max_depth()
                balanced = tree.is_balanced()

                assert len(levels) > 0
                assert depth > 0
                assert isinstance(balanced, bool)

    def test_empty_tree_scenario(self):
        """Test empty tree scenario."""
        tree = BinaryTree.from_list([])
        assert tree.level_order_traversal() == []
        assert tree.max_depth() == 0
        assert tree.is_balanced() is True

    def test_output_contains_expected_sections(self, capsys):
        """Test that main output contains all expected sections."""
        main()
        captured = capsys.readouterr()
        output = captured.out

        expected_sections = [
            "1. Creating Binary Trees",
            "2. DFS Traversals",
            "3. BFS Traversal (Level Order)",
            "4. Tree Properties",
            "5. Path Sum Problems",
            "6. Tree Views",
            "7. Lowest Common Ancestor",
            "8. Tree Serialization",
            "9. Common Interview Scenarios",
        ]

        for section in expected_sections:
            assert section in output

    def test_no_errors_in_output(self, capsys):
        """Test that no errors or exceptions appear in the output."""
        main()
        captured = capsys.readouterr()
        output = captured.out.lower()

        error_keywords = ["error", "exception", "traceback", "failed"]
        for keyword in error_keywords:
            assert keyword not in output

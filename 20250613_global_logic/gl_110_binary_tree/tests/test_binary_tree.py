"""Tests for binary tree data structures and algorithms."""

import pytest
from binary_tree_prep.binary_tree import TreeNode, BinaryTree


class TestTreeNode:
    def test_tree_node_creation(self):
        node = TreeNode(5)
        assert node.val == 5
        assert node.left is None
        assert node.right is None

    def test_tree_node_with_children(self):
        left = TreeNode(3)
        right = TreeNode(7)
        node = TreeNode(5, left, right)
        assert node.val == 5
        assert node.left == left
        assert node.right == right

    def test_tree_node_repr(self):
        node = TreeNode(5)
        assert repr(node) == "TreeNode(5)"


class TestBinaryTree:
    def test_empty_tree_creation(self):
        tree = BinaryTree()
        assert tree.root is None

    def test_tree_with_root(self):
        root = TreeNode(5)
        tree = BinaryTree(root)
        assert tree.root == root

    def test_from_list_empty(self):
        tree = BinaryTree.from_list([])
        assert tree.root is None

        tree = BinaryTree.from_list([None])
        assert tree.root is None

    def test_from_list_single_node(self):
        tree = BinaryTree.from_list([5])
        assert tree.root.val == 5
        assert tree.root.left is None
        assert tree.root.right is None

    def test_from_list_complete_tree(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert tree.root.val == 1
        assert tree.root.left.val == 2
        assert tree.root.right.val == 3
        assert tree.root.left.left.val == 4
        assert tree.root.left.right.val == 5
        assert tree.root.right.left.val == 6
        assert tree.root.right.right.val == 7

    def test_from_list_with_none_values(self):
        tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
        assert tree.root.val == 3
        assert tree.root.left.val == 9
        assert tree.root.right.val == 20
        assert tree.root.left.left is None
        assert tree.root.left.right is None
        assert tree.root.right.left.val == 15
        assert tree.root.right.right.val == 7


class TestTraversals:
    @pytest.fixture
    def sample_tree(self):
        return BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])

    def test_inorder_traversal_empty(self):
        tree = BinaryTree()
        assert tree.inorder_traversal() == []

    def test_inorder_traversal(self, sample_tree):
        assert sample_tree.inorder_traversal() == [4, 2, 5, 1, 6, 3, 7]

    def test_preorder_traversal_empty(self):
        tree = BinaryTree()
        assert tree.preorder_traversal() == []

    def test_preorder_traversal(self, sample_tree):
        assert sample_tree.preorder_traversal() == [1, 2, 4, 5, 3, 6, 7]

    def test_postorder_traversal_empty(self):
        tree = BinaryTree()
        assert tree.postorder_traversal() == []

    def test_postorder_traversal(self, sample_tree):
        assert sample_tree.postorder_traversal() == [4, 5, 2, 6, 7, 3, 1]

    def test_level_order_traversal_empty(self):
        tree = BinaryTree()
        assert tree.level_order_traversal() == []

    def test_level_order_traversal(self, sample_tree):
        expected = [[1], [2, 3], [4, 5, 6, 7]]
        assert sample_tree.level_order_traversal() == expected

    def test_level_order_traversal_sparse(self):
        tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
        expected = [[3], [9, 20], [15, 7]]
        assert tree.level_order_traversal() == expected


class TestTreeProperties:
    def test_max_depth_empty(self):
        tree = BinaryTree()
        assert tree.max_depth() == 0

    def test_max_depth_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.max_depth() == 1

    def test_max_depth_balanced(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert tree.max_depth() == 3

    def test_max_depth_unbalanced(self):
        tree = BinaryTree.from_list([1, 2, None, 3, None, 4])
        assert tree.max_depth() == 4

    def test_min_depth_empty(self):
        tree = BinaryTree()
        assert tree.min_depth() == 0

    def test_min_depth_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.min_depth() == 1

    def test_min_depth_balanced(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert tree.min_depth() == 3

    def test_min_depth_unbalanced(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, None, None, 7])
        assert tree.min_depth() == 3

    def test_diameter_empty(self):
        tree = BinaryTree()
        assert tree.diameter() == 0

    def test_diameter_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.diameter() == 0

    def test_diameter_balanced(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, 5])
        assert tree.diameter() == 3

    def test_diameter_unbalanced(self):
        tree = BinaryTree.from_list([1, 2, None, 3, None, 4])
        assert tree.diameter() == 3

    def test_is_balanced_empty(self):
        tree = BinaryTree()
        assert tree.is_balanced() is True

    def test_is_balanced_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.is_balanced() is True

    def test_is_balanced_true(self):
        tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])
        assert tree.is_balanced() is True

    def test_is_balanced_false(self):
        tree = BinaryTree.from_list([1, 2, None, 3, None, 4])
        assert tree.is_balanced() is False


class TestPathSum:
    def test_path_sum_empty(self):
        tree = BinaryTree()
        assert tree.path_sum_exists(0) is False

    def test_path_sum_single_node_match(self):
        tree = BinaryTree.from_list([5])
        assert tree.path_sum_exists(5) is True

    def test_path_sum_single_node_no_match(self):
        tree = BinaryTree.from_list([5])
        assert tree.path_sum_exists(10) is False

    def test_path_sum_exists(self):
        tree = BinaryTree.from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
        assert tree.path_sum_exists(22) is True

    def test_path_sum_not_exists(self):
        tree = BinaryTree.from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
        assert tree.path_sum_exists(100) is False


class TestRightSideView:
    def test_right_side_view_empty(self):
        tree = BinaryTree()
        assert tree.right_side_view() == []

    def test_right_side_view_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.right_side_view() == [1]

    def test_right_side_view_complete(self):
        tree = BinaryTree.from_list([1, 2, 3, None, 5, None, 4])
        assert tree.right_side_view() == [1, 3, 4]

    def test_right_side_view_left_skewed(self):
        tree = BinaryTree.from_list([1, 2, None, 3])
        assert tree.right_side_view() == [1, 2, 3]


class TestLowestCommonAncestor:
    def test_lca_same_node(self):
        tree = BinaryTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        node5 = self._find_node(tree.root, 5)
        lca = tree.lowest_common_ancestor(node5, node5)
        assert lca.val == 5

    def test_lca_parent_child(self):
        tree = BinaryTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        node5 = self._find_node(tree.root, 5)
        node6 = self._find_node(tree.root, 6)
        lca = tree.lowest_common_ancestor(node5, node6)
        assert lca.val == 5

    def test_lca_different_subtrees(self):
        tree = BinaryTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
        node5 = self._find_node(tree.root, 5)
        node1 = self._find_node(tree.root, 1)
        lca = tree.lowest_common_ancestor(node5, node1)
        assert lca.val == 3

    def _find_node(self, root, val):
        if not root:
            return None
        if root.val == val:
            return root
        return self._find_node(root.left, val) or self._find_node(root.right, val)


class TestSerialization:
    def test_serialize_empty(self):
        tree = BinaryTree()
        assert tree.serialize() == "null"

    def test_serialize_single_node(self):
        tree = BinaryTree.from_list([1])
        assert tree.serialize() == "1,null,null"

    def test_serialize_deserialize_roundtrip(self):
        original = BinaryTree.from_list([1, 2, 3, None, None, 4, 5])
        serialized = original.serialize()
        deserialized = BinaryTree.deserialize(serialized)

        assert original.level_order_traversal() == deserialized.level_order_traversal()
        assert original.inorder_traversal() == deserialized.inorder_traversal()

    def test_deserialize_empty(self):
        tree = BinaryTree.deserialize("null")
        assert tree.root is None

    def test_deserialize_single_node(self):
        tree = BinaryTree.deserialize("1,null,null")
        assert tree.root.val == 1
        assert tree.root.left is None
        assert tree.root.right is None


class TestEdgeCases:
    """Test edge cases class."""

    def test_negative_values(self):
        """Test negative values."""
        tree = BinaryTree.from_list([-1, -2, -3])
        assert tree.inorder_traversal() == [-2, -1, -3]
        assert tree.max_depth() == 2

    def test_zero_values(self):
        """Test zero values."""
        tree = BinaryTree.from_list([0, 0, 0])
        assert tree.inorder_traversal() == [0, 0, 0]
        assert tree.path_sum_exists(0) is True

    def test_large_tree(self):
        """Test large tree."""
        values = list(range(1, 32))
        tree = BinaryTree.from_list(values)
        assert tree.max_depth() == 5
        assert len(tree.inorder_traversal()) == 31

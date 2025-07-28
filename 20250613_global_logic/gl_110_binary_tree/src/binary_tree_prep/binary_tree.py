"""Binary Tree data structures and algorithms for interview preparation."""

from collections import deque
from typing import Optional


class TreeNode:
    """A node in a binary tree."""

    def __init__(
        self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None
    ):
        """Initialize a tree node."""
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        """Return string representation of the node."""
        return f"TreeNode({self.val})"


class BinaryTree:
    """Binary tree with common algorithms and operations."""

    def __init__(self, root: TreeNode | None = None):
        """Initialize a binary tree."""
        self.root = root

    @classmethod
    def from_list(cls, values: list[int | None]) -> "BinaryTree":
        """Create binary tree from level-order list representation."""
        if not values or values[0] is None:
            return cls()

        root = TreeNode(values[0])
        queue = deque([root])
        i = 1

        while queue and i < len(values):
            node = queue.popleft()

            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1

            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1

        return cls(root)

    def inorder_traversal(self) -> list[int]:
        """DFS: Left -> Root -> Right."""
        result = []

        def inorder(node: TreeNode | None):
            if node:
                inorder(node.left)
                result.append(node.val)
                inorder(node.right)

        inorder(self.root)
        return result

    def preorder_traversal(self) -> list[int]:
        """DFS: Root -> Left -> Right."""
        result = []

        def preorder(node: TreeNode | None):
            if node:
                result.append(node.val)
                preorder(node.left)
                preorder(node.right)

        preorder(self.root)
        return result

    def postorder_traversal(self) -> list[int]:
        """DFS: Left -> Right -> Root."""
        result = []

        def postorder(node: TreeNode | None):
            if node:
                postorder(node.left)
                postorder(node.right)
                result.append(node.val)

        postorder(self.root)
        return result

    def level_order_traversal(self) -> list[list[int]]:
        """BFS: Level by level traversal."""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)
            level_values = []

            for _ in range(level_size):
                node = queue.popleft()
                level_values.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_values)

        return result

    def max_depth(self) -> int:
        """Calculate maximum depth/height of the tree."""

        def depth(node: TreeNode | None) -> int:
            if not node:
                return 0
            return 1 + max(depth(node.left), depth(node.right))

        return depth(self.root)

    def min_depth(self) -> int:
        """Calculate minimum depth of the tree."""
        if not self.root:
            return 0

        queue = deque([(self.root, 1)])

        while queue:
            node, level = queue.popleft()

            if not node.left and not node.right:
                return level

            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))

        return 0

    def diameter(self) -> int:
        """Calculate diameter of the tree (longest path between any two nodes)."""
        self.max_diameter = 0

        def height(node: TreeNode | None) -> int:
            if not node:
                return 0

            left_height = height(node.left)
            right_height = height(node.right)

            self.max_diameter = max(self.max_diameter, left_height + right_height)

            return 1 + max(left_height, right_height)

        height(self.root)
        return self.max_diameter

    def is_balanced(self) -> bool:
        """Check if tree is height-balanced."""

        def check_balance(node: TreeNode | None) -> tuple[bool, int]:
            if not node:
                return True, 0

            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)

            balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
            height = 1 + max(left_height, right_height)

            return balanced, height

        balanced, _ = check_balance(self.root)
        return balanced

    def lowest_common_ancestor(self, p: TreeNode, q: TreeNode) -> TreeNode | None:
        """Find lowest common ancestor of two nodes."""

        def lca(node: TreeNode | None) -> TreeNode | None:
            if node in (p, q) or not node:
                return node

            left = lca(node.left)
            right = lca(node.right)

            if left and right:
                return node

            return left or right

        return lca(self.root)

    def path_sum_exists(self, target_sum: int) -> bool:
        """Check if there exists a root-to-leaf path with given sum."""

        def has_path_sum(node: TreeNode | None, remaining: int) -> bool:
            if not node:
                return False

            remaining -= node.val

            if not node.left and not node.right:
                return remaining == 0

            return has_path_sum(node.left, remaining) or has_path_sum(node.right, remaining)

        return has_path_sum(self.root, target_sum)

    def right_side_view(self) -> list[int]:
        """Return the values visible from the right side (rightmost node at each level)."""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            level_size = len(queue)

            for i in range(level_size):
                node = queue.popleft()

                if i == level_size - 1:
                    result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def serialize(self) -> str:
        """Serialize tree to string."""

        def preorder(node: TreeNode | None) -> list[str]:
            if not node:
                return ["null"]
            return [str(node.val)] + preorder(node.left) + preorder(node.right)

        return ",".join(preorder(self.root))

    @classmethod
    def deserialize(cls, data: str) -> "BinaryTree":
        """Deserialize string to tree."""

        def build_tree(values: list[str]) -> TreeNode | None:
            val = next(values)
            if val == "null":
                return None

            node = TreeNode(int(val))
            node.left = build_tree(values)
            node.right = build_tree(values)
            return node

        values = iter(data.split(","))
        root = build_tree(values)
        return cls(root)

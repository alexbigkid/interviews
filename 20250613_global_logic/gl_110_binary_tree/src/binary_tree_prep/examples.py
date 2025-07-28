#!/usr/bin/env python3
"""Binary Tree Interview Preparation Examples.

This file demonstrates common binary tree algorithms and their usage.
"""

from .binary_tree import BinaryTree, TreeNode


def main():
    """Run binary tree examples and demonstrations."""
    print("=== Binary Tree Interview Preparation Examples ===\n")

    # Example 1: Creating a binary tree
    print("1. Creating Binary Trees")
    print("-" * 30)

    # Method 1: Using list representation
    tree1 = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
    print("Tree from list [3, 9, 20, None, None, 15, 7]:")
    print(f"Level order: {tree1.level_order_traversal()}")

    # Method 2: Manual construction
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    tree2 = BinaryTree(root)
    print(f"\nManually constructed tree: {tree2.level_order_traversal()}")

    print("\n" + "=" * 50 + "\n")

    # Example 2: DFS Traversals
    print("2. DFS Traversals")
    print("-" * 30)

    tree = BinaryTree.from_list([1, 2, 3, 4, 5, 6, 7])
    print("Tree:", tree.level_order_traversal())
    print(f"Inorder (Left-Root-Right):   {tree.inorder_traversal()}")
    print(f"Preorder (Root-Left-Right):  {tree.preorder_traversal()}")
    print(f"Postorder (Left-Right-Root): {tree.postorder_traversal()}")

    print("\n" + "=" * 50 + "\n")

    # Example 3: BFS Traversal
    print("3. BFS Traversal (Level Order)")
    print("-" * 30)

    tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
    levels = tree.level_order_traversal()
    print("Tree:", levels)
    for i, level in enumerate(levels):
        print(f"Level {i}: {level}")

    print("\n" + "=" * 50 + "\n")

    # Example 4: Tree Properties
    print("4. Tree Properties")
    print("-" * 30)

    tree = BinaryTree.from_list([3, 9, 20, None, None, 15, 7])
    print(f"Tree: {tree.level_order_traversal()}")
    print(f"Max depth: {tree.max_depth()}")
    print(f"Min depth: {tree.min_depth()}")
    print(f"Diameter: {tree.diameter()}")
    print(f"Is balanced: {tree.is_balanced()}")

    print("\n" + "=" * 50 + "\n")

    # Example 5: Path Sum
    print("5. Path Sum Problems")
    print("-" * 30)

    tree = BinaryTree.from_list([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    print(f"Tree: {tree.level_order_traversal()}")
    target = 22
    print(f"Has path sum {target}: {tree.path_sum_exists(target)}")

    print("\n" + "=" * 50 + "\n")

    # Example 6: Tree Views
    print("6. Tree Views")
    print("-" * 30)

    tree = BinaryTree.from_list([1, 2, 3, None, 5, None, 4])
    print(f"Tree: {tree.level_order_traversal()}")
    print(f"Right side view: {tree.right_side_view()}")

    print("\n" + "=" * 50 + "\n")

    # Example 7: Lowest Common Ancestor
    print("7. Lowest Common Ancestor")
    print("-" * 30)

    tree = BinaryTree.from_list([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    print(f"Tree: {tree.level_order_traversal()}")

    # Find nodes with values 5 and 1
    def find_node(root, val):
        if not root:
            return None
        if root.val == val:
            return root
        return find_node(root.left, val) or find_node(root.right, val)

    node5 = find_node(tree.root, 5)
    node1 = find_node(tree.root, 1)
    lca = tree.lowest_common_ancestor(node5, node1)
    print(f"LCA of nodes 5 and 1: {lca.val if lca else None}")

    print("\n" + "=" * 50 + "\n")

    # Example 8: Serialization
    print("8. Tree Serialization")
    print("-" * 30)

    tree = BinaryTree.from_list([1, 2, 3, None, None, 4, 5])
    print(f"Original tree: {tree.level_order_traversal()}")

    serialized = tree.serialize()
    print(f"Serialized: {serialized}")

    deserialized_tree = BinaryTree.deserialize(serialized)
    print(f"Deserialized tree: {deserialized_tree.level_order_traversal()}")

    print("\n" + "=" * 50 + "\n")

    # Common Interview Scenarios
    print("9. Common Interview Scenarios")
    print("-" * 30)

    scenarios = [
        ("Complete Binary Tree", [1, 2, 3, 4, 5, 6, 7]),
        ("Perfect Binary Tree", [1, 2, 3, 4, 5, 6, 7]),
        ("Balanced Binary Tree", [1, 2, 3, 4, 5, 6]),
        ("Unbalanced Binary Tree", [1, 2, None, 3, None, 4]),
        ("Left Skewed Tree", [1, 2, None, 3, None, 4]),
        ("Right Skewed Tree", [1, None, 2, None, None, None, 3]),
        ("Single Node", [1]),
        ("Empty Tree", []),
    ]

    for name, values in scenarios:
        if values:
            tree = BinaryTree.from_list(values)
            print(f"{name}:")
            print(f"  Structure: {tree.level_order_traversal()}")
            print(f"  Height: {tree.max_depth()}, Balanced: {tree.is_balanced()}")
        else:
            print(f"{name}: Empty tree")
        print()


if __name__ == "__main__":
    main()

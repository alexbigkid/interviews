def invert_binary_tree(tree):
    if tree:
        left = tree.left
        right = tree.right
        tree.left = right
        tree.right = left
        invert_binary_tree(tree.left)
        invert_binary_tree(tree.right)

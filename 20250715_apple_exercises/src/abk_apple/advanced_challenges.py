"""
Advanced Level Python Challenges for Apple Interview Preparation
"""


# Helper class for binary tree problems
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Helper class for linked list problems
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def serialize(root: TreeNode) -> str:
    """
    Challenge: Serialize Binary Tree
    Serialize a binary tree to a single string using preorder traversal.

    Example:
    Input: root = [1,2,3,null,null,4,5]
    Output: "1,2,null,null,3,4,null,null,5,null,null"

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return "null"

    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"


def deserialize(data: str) -> TreeNode:
    """
    Challenge: Deserialize Binary Tree
    Deserialize a string back to a binary tree using preorder traversal.

    Example:
    Input: "1,2,null,null,3,4,null,null,5,null,null"
    Output: TreeNode representing [1,2,3,null,null,4,5]

    Time Complexity: O(n)
    Space Complexity: O(n)
    """

    def build_tree():
        val = next(nodes)
        if val == "null":
            return None

        node = TreeNode(int(val))
        node.left = build_tree()
        node.right = build_tree()
        return node

    nodes = iter(data.split(","))
    return build_tree()


def word_ladder(beginWord: str, endWord: str, wordList: list[str]) -> int:
    """
    Challenge: Word Ladder
    A transformation sequence from word beginWord to word endWord using a dictionary wordList
    is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

    - Every adjacent pair of words differs by a single letter.
    - Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
    - sk == endWord

    Given two words, beginWord and endWord, and a dictionary wordList, return the number of words
    in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

    Example:
    Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> "cog", which is 5 words long.

    Time Complexity: O(M^2 * N) where M is the length of each word and N is the total number of words
    Space Complexity: O(M^2 * N)
    """
    from collections import deque

    if endWord not in wordList:
        return 0

    wordSet = set(wordList)
    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        if word == endWord:
            return length

        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                new_word = word[:i] + c + word[i + 1 :]
                if new_word in wordSet and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))

    return 0


def alien_dictionary(words):
    """
    Challenge: Alien Dictionary
    There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you.

    You are given a list of strings words from the alien language's dictionary, where the strings in words are
    sorted lexicographically by the rules of this new language.

    Return a string of the unique letters in the new alien language sorted in lexicographically increasing order
    by the new language's rules. If there is no solution, return "". If there are multiple solutions, return any of them.

    Example:
    Input: words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"

    Time Complexity: O(C) where C is the total length of all words
    Space Complexity: O(1) or O(U + min(U^2, N)) where U is the number of unique letters and N is the number of words
    """
    from collections import defaultdict, deque

    # Build adjacency list and in-degree count
    graph = defaultdict(set)
    in_degree = defaultdict(int)

    # Initialize in-degree for all characters
    for word in words:
        for char in word:
            in_degree[char] = 0

    # Build graph by comparing adjacent words
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]

        # Check if word1 is a prefix of word2 but longer (invalid)
        if len(word1) > len(word2) and word1.startswith(word2):
            return ""

        # Find first differing character
        for j in range(min(len(word1), len(word2))):
            if word1[j] != word2[j]:
                if word2[j] not in graph[word1[j]]:
                    graph[word1[j]].add(word2[j])
                    in_degree[word2[j]] += 1
                break

    # Topological sort using Kahn's algorithm
    queue = deque([char for char in in_degree if in_degree[char] == 0])
    result = []

    while queue:
        char = queue.popleft()
        result.append(char)

        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all characters are processed (no cycle)
    if len(result) != len(in_degree):
        return ""

    return "".join(result)


def median_from_data_stream():
    """
    Challenge: Find Median from Data Stream
    The median is the middle value in an ordered integer list. If the size of the list is even,
    there is no middle value and the median is the mean of the two middle values.

    Implement the MedianFinder class:
    - MedianFinder() initializes the MedianFinder object.
    - void addNum(int num) adds the integer num from the data stream to the data structure.
    - double findMedian() returns the median of all elements so far.

    Example:
    Input: ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
           [[], [1], [2], [], [3], []]
    Output: [null, null, null, 1.5, null, 2.0]

    Time Complexity: O(log n) for addNum, O(1) for findMedian
    Space Complexity: O(n)
    """

    class MedianFinder:
        def __init__(self):
            import heapq

            self.small = []  # max heap (negate values)
            self.large = []  # min heap
            self.heapq = heapq

        def addNum(self, num):
            # Add to max heap (small) first
            self.heapq.heappush(self.small, -num)

            # Ensure max heap element <= min heap element
            if self.small and self.large and (-self.small[0] > self.large[0]):
                val = -self.heapq.heappop(self.small)
                self.heapq.heappush(self.large, val)

            # Balance the heaps
            if len(self.small) > len(self.large) + 1:
                val = -self.heapq.heappop(self.small)
                self.heapq.heappush(self.large, val)
            elif len(self.large) > len(self.small) + 1:
                val = self.heapq.heappop(self.large)
                self.heapq.heappush(self.small, -val)

        def findMedian(self):
            if len(self.small) > len(self.large):
                return float(-self.small[0])
            elif len(self.large) > len(self.small):
                return float(self.large[0])
            else:
                return (-self.small[0] + self.large[0]) / 2.0

    return MedianFinder


def merge_k_sorted_lists(lists):
    """
    Challenge: Merge k Sorted Lists
    You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
    Merge all the linked-lists into one sorted linked-list and return it.

    Example:
    Input: lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]

    Time Complexity: O(n log k) where n is the total number of nodes and k is the number of lists
    Space Complexity: O(log k)
    """
    import heapq

    if not lists:
        return None

    # Remove empty lists
    lists = [lst for lst in lists if lst]
    if not lists:
        return None

    # Create min heap with (value, index, node)
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))

    dummy = ListNode(0)
    current = dummy

    while heap:
        val, list_idx, node = heapq.heappop(heap)
        current.next = node
        current = current.next

        # Add next node from the same list
        if node.next:
            heapq.heappush(heap, (node.next.val, list_idx, node.next))

    return dummy.next


def lru_cache(capacity):
    """
    Challenge: LRU Cache
    Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

    Implement the LRUCache class:
    - LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
    - int get(int key) Return the value of the key if the key exists, otherwise return -1.
    - void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache.
      If the number of keys exceeds the capacity from this operation, evict the least recently used key.

    The functions get and put must each run in O(1) average time complexity.

    Example:
    Input: ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
           [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output: [null, null, null, 1, null, -1, null, -1, 3, 4]

    Time Complexity: O(1) for both get and put operations
    Space Complexity: O(capacity)
    """

    class LRUCache:
        def __init__(self, capacity):
            self.capacity = capacity
            self.cache = {}

            # Create dummy head and tail nodes
            self.head = ListNode(0, 0)
            self.tail = ListNode(0, 0)
            self.head.next = self.tail
            self.tail.prev = self.head

        def _add_node(self, node):
            """Add node right after head"""
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node

        def _remove_node(self, node):
            """Remove an existing node from the linked list"""
            prev_node = node.prev
            new_node = node.next
            prev_node.next = new_node
            new_node.prev = prev_node

        def _move_to_head(self, node):
            """Move node to head (mark as recently used)"""
            self._remove_node(node)
            self._add_node(node)

        def _pop_tail(self):
            """Remove last node (least recently used)"""
            lru_node = self.tail.prev
            self._remove_node(lru_node)
            return lru_node

        def get(self, key):
            node = self.cache.get(key)
            if node:
                # Move to head (mark as recently used)
                self._move_to_head(node)
                return node.val
            return -1

        def put(self, key, value):
            node = self.cache.get(key)

            if node:
                # Update existing node
                node.val = value
                self._move_to_head(node)
            else:
                # Add new node
                new_node = ListNode(key, value)

                if len(self.cache) >= self.capacity:
                    # Remove LRU node
                    tail = self._pop_tail()
                    del self.cache[tail.key]

                self.cache[key] = new_node
                self._add_node(new_node)

    # Enhanced ListNode for LRU
    class ListNode:
        def __init__(self, key, val):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    return LRUCache


def trap_rain_water(height):
    """
    Challenge: Trapping Rain Water
    Given n non-negative integers representing an elevation map where the width of each bar is 1,
    compute how much water it can trap after raining.

    Example:
    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: The above elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1].
    In this case, 6 units of rain water are being trapped.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not height or len(height) < 3:
        return 0

    left = 0
    right = len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water


def sliding_window_maximum(nums, k):
    """
    Challenge: Sliding Window Maximum
    You are given an array of integers nums, there is a sliding window of size k which is moving
    from the very left of the array to the very right. You can only see the k numbers in the window.
    Each time the sliding window moves right by one position.

    Return the max sliding window.

    Example:
    Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [3,3,5,5,6,7]

    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    from collections import deque

    if not nums or k == 0:
        return []

    dq = deque()  # Store indices
    result = []

    for i in range(len(nums)):
        # Remove indices that are out of current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove indices of smaller elements from the back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Add to result when window is complete
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Problem-Solving Patterns and Complexity Analysis

This comprehensive guide provides visual frameworks for recognizing patterns and analyzing complexity in technical interviews.

## Master Pattern Recognition Framework

```mermaid
flowchart TD
    Problem[Problem Statement] --> InputAnalysis{Analyze Input}
    
    InputAnalysis -->|Single Array/String| SingleDS[Single Data Structure Patterns]
    InputAnalysis -->|Two Arrays/Strings| TwoDS[Two Data Structure Patterns]
    InputAnalysis -->|Tree/Graph| TreeGraph[Tree/Graph Patterns]
    InputAnalysis -->|Multiple Inputs| Complex[Complex Problem Patterns]
    
    SingleDS --> SinglePatterns["• Sliding Window<br/>• Two Pointers<br/>• Fast/Slow Pointers<br/>• Cyclic Sort<br/>• In-place Reversal"]
    
    TwoDS --> TwoPatterns["• Two Pointers<br/>• Merge Intervals<br/>• Binary Search<br/>• Top K Elements<br/>• K-way Merge"]
    
    TreeGraph --> TreePatterns["• DFS/BFS<br/>• Tree Traversal<br/>• Island Problems<br/>• Topological Sort<br/>• Union Find"]
    
    Complex --> ComplexPatterns["• Dynamic Programming<br/>• Backtracking<br/>• Modified Binary Search<br/>• Substring Problems<br/>• Interval Problems"]
```

## Pattern-to-Problem Mapping

### Sliding Window Pattern

```mermaid
graph TB
    subgraph "Sliding Window Recognition"
        Trigger["Triggers:<br/>• Contiguous subarray/substring<br/>• 'Maximum/minimum subarray of size K'<br/>• 'Longest substring with K distinct characters'<br/>• 'Find all anagrams'"]
        
        FixedSize["Fixed Size Window:<br/>• Maximum sum of K elements<br/>• Average of all contiguous subarrays<br/>• First negative in every window"]
        
        VariableSize["Variable Size Window:<br/>• Longest substring without repeating<br/>• Minimum window substring<br/>• Fruits into baskets"]
        
        Trigger --> FixedSize
        Trigger --> VariableSize
    end
    
    subgraph "Implementation Template"
        Template["
        def sliding_window(arr, k):
            window_start = 0
            result = []
            
            for window_end in range(len(arr)):
                # Expand window
                # Add arr[window_end] to window
                
                if window_end >= k - 1:  # Window size reached
                    # Process current window
                    # Add result
                    
                    # Shrink window
                    # Remove arr[window_start] from window
                    window_start += 1
            
            return result
        "]
    end
```

### Two Pointers Pattern

```mermaid
graph TB
    subgraph "Two Pointers Variations"
        Opposite["Opposite Direction:<br/>• Two Sum in sorted array<br/>• Valid palindrome<br/>• Container with most water"]
        
        SameDirection["Same Direction:<br/>• Remove duplicates<br/>• Move zeros<br/>• Sort colors (Dutch flag)"]
        
        FastSlow["Fast & Slow:<br/>• Linked list cycle<br/>• Find middle of linked list<br/>• Happy number"]
    end
    
    subgraph "Decision Tree"
        Start[Array Problem] --> Sorted{Is array sorted?}
        
        Sorted -->|Yes| Target{Looking for target sum?}
        Sorted -->|No| InPlace{Need in-place operation?}
        
        Target -->|Yes| TwoSum[Two Sum Pattern]
        Target -->|No| Palindrome[Palindrome Check Pattern]
        
        InPlace -->|Yes| DutchFlag[Dutch Flag Pattern]
        InPlace -->|No| OtherPattern[Consider other patterns]
    end
```

### Binary Search Pattern

```mermaid
graph TB
    subgraph "Binary Search Recognition"
        Sorted["Prerequisites:<br/>• Sorted array/range<br/>• Monotonic function<br/>• Search space can be divided"]
        
        Variants["Common Variants:<br/>• Find exact element<br/>• Find first/last occurrence<br/>• Find peak element<br/>• Search in rotated array<br/>• Find minimum in range"]
        
        Template["
        def binary_search(arr, target):
            left, right = 0, len(arr) - 1
            
            while left <= right:
                mid = left + (right - left) // 2
                
                if condition(mid):
                    # Answer might be at mid or left side
                    right = mid - 1
                    result = mid  # Save potential answer
                else:
                    # Answer is on right side
                    left = mid + 1
            
            return result
        "]
    end
```

## Dynamic Programming Patterns

### DP Problem Classification

```mermaid
mindmap
  root((DP Patterns))
    Linear DP
      Fibonacci-like
        Climbing stairs
        House robber
        Decode ways
      Array processing
        Maximum subarray
        Jump game
        Stock trading
    2D DP
      Grid paths
        Unique paths
        Minimum path sum
        Dungeon game
      String matching
        Edit distance
        LCS/LIS
        Palindrome problems
    Tree DP
      Binary tree problems
        House robber III
        Binary tree cameras
        Maximum path sum
    Interval DP
      Matrix chain multiplication
      Palindrome partitioning
      Burst balloons
    State Machine DP
      Best time to buy/sell stock
      Paint house
      Paint fence
```

### DP Recognition Framework

```mermaid
flowchart TD
    Problem[Problem Statement] --> Optimization{Optimization Problem?}
    
    Optimization -->|Yes| Subproblems{Has overlapping subproblems?}
    Optimization -->|No| OtherApproach[Consider greedy/other approaches]
    
    Subproblems -->|Yes| OptimalSubstructure{Optimal substructure?}
    Subproblems -->|No| Divide[Divide & Conquer]
    
    OptimalSubstructure -->|Yes| DPType{What type of DP?}
    OptimalSubstructure -->|No| Greedy[Greedy Algorithm]
    
    DPType --> Linear[Linear DP<br/>• 1D state<br/>• Previous decisions matter]
    DPType --> Grid[2D/Grid DP<br/>• 2D state space<br/>• Path-based problems]
    DPType --> Interval[Interval DP<br/>• Range-based state<br/>• Merge/split decisions]
    DPType --> StateMachine[State Machine DP<br/>• Multiple states per position<br/>• State transitions]
```

## Complexity Analysis Framework

### Time Complexity Hierarchy

```mermaid
graph TB
    subgraph "Common Time Complexities (Best to Worst)"
        O1["O(1) - Constant"]
        OlogN["O(log n) - Logarithmic"]
        ON["O(n) - Linear"]
        ONlogN["O(n log n) - Linearithmic"]
        ON2["O(n²) - Quadratic"]
        ON3["O(n³) - Cubic"]
        O2N["O(2ⁿ) - Exponential"]
        ONFact["O(n!) - Factorial"]
        
        O1 --> OlogN --> ON --> ONlogN --> ON2 --> ON3 --> O2N --> ONFact
    end
    
    subgraph "Algorithm Examples"
        O1 -.-> E1["Array access, HashMap operations"]
        OlogN -.-> E2["Binary search, balanced tree operations"]
        ON -.-> E3["Linear search, array traversal"]
        ONlogN -.-> E4["Merge sort, heap sort"]
        ON2 -.-> E5["Bubble sort, nested loops"]
        ON3 -.-> E6["Matrix multiplication"]
        O2N -.-> E7["Recursive Fibonacci, subset generation"]
        ONFact -.-> E8["Permutation generation"]
    end
```

### Space Complexity Analysis

```mermaid
graph TB
    subgraph "Space Complexity Categories"
        Input["Input Space<br/>• Space used by input data<br/>• Usually not counted in analysis"]
        
        Auxiliary["Auxiliary Space<br/>• Extra space used by algorithm<br/>• This is what we analyze"]
        
        Output["Output Space<br/>• Space used by output<br/>• Sometimes counted separately"]
    end
    
    subgraph "Common Space Patterns"
        Constant["O(1) - Constant Extra Space<br/>• Few variables<br/>• In-place algorithms<br/>• Iterative solutions"]
        
        Linear["O(n) - Linear Extra Space<br/>• Single array/list<br/>• Hash table with n elements<br/>• Recursion depth n"]
        
        Quadratic["O(n²) - Quadratic Extra Space<br/>• 2D array<br/>• Graph adjacency matrix<br/>• DP table"]
    end
```

### Amortized Analysis

```mermaid
graph TB
    subgraph "Amortized Analysis Concepts"
        Definition["Amortized Analysis:<br/>Average time per operation<br/>over a sequence of operations"]
        
        Methods["Analysis Methods:<br/>• Aggregate method<br/>• Accounting method<br/>• Potential method"]
        
        Examples["Common Examples:<br/>• Dynamic array resizing<br/>• Union-Find with path compression<br/>• Splay trees"]
    end
    
    subgraph "Dynamic Array Example"
        Operations["Sequence: n insertions into dynamic array"]
        
        Individual["Individual costs:<br/>• Most insertions: O(1)<br/>• Resize operations: O(n)"]
        
        Amortized["Amortized cost:<br/>• Total cost: O(n)<br/>• Average per operation: O(1)"]
        
        Operations --> Individual --> Amortized
    end
```

## Problem Classification by Constraints

### Constraint-Based Strategy Selection

```mermaid
flowchart TD
    Constraints[Problem Constraints] --> Size{Input Size}
    
    Size -->|n ≤ 20| Exponential[O(2ⁿ) or O(n!) acceptable<br/>• Backtracking<br/>• Complete search<br/>• Dynamic programming with bitmask]
    
    Size -->|n ≤ 100| Cubic[O(n³) acceptable<br/>• Floyd-Warshall<br/>• Matrix multiplication<br/>• Triple nested loops]
    
    Size -->|n ≤ 1000| Quadratic[O(n²) acceptable<br/>• Bubble sort variations<br/>• Simple DP<br/>• Nested loop solutions]
    
    Size -->|n ≤ 10⁵| Linearithmic[O(n log n) needed<br/>• Merge sort<br/>• Binary search applications<br/>• Heap operations]
    
    Size -->|n ≤ 10⁶| Linear[O(n) or O(n log n) required<br/>• Linear scan<br/>• Hash table operations<br/>• Efficient sorting]
    
    Size -->|n > 10⁶| Sublinear[Better than O(n) needed<br/>• O(log n) binary search<br/>• O(1) mathematical solutions<br/>• Specialized algorithms]
```

### Memory Constraint Analysis

```mermaid
graph TB
    subgraph "Memory Constraint Strategies"
        Tight["Tight Memory Constraints<br/>• Prefer O(1) space algorithms<br/>• In-place modifications<br/>• Bit manipulation tricks<br/>• Streaming algorithms"]
        
        Moderate["Moderate Memory<br/>• O(n) space acceptable<br/>• Hash tables, auxiliary arrays<br/>• Standard DP approaches"]
        
        Generous["Generous Memory<br/>• O(n²) or higher space OK<br/>• 2D DP tables<br/>• Preprocessing structures<br/>• Memoization"]
    end
    
    subgraph "Space-Time Tradeoffs"
        Precompute["Precomputation:<br/>• Use extra space for faster queries<br/>• Prefix sums, lookup tables"]
        
        Streaming["Streaming/Online:<br/>• Process data as it arrives<br/>• Constant space requirement"]
        
        Batch["Batch Processing:<br/>• Process in chunks<br/>• Balance memory usage"]
    end
```

## Advanced Pattern Recognition

### Interval Problems Pattern

```mermaid
graph TB
    subgraph "Interval Problem Types"
        Merge["Merge Overlapping Intervals<br/>• Sort by start time<br/>• Merge consecutive overlaps"]
        
        Insert["Insert Interval<br/>• Find position to insert<br/>• Merge with overlapping intervals"]
        
        NonOverlap["Non-overlapping Intervals<br/>• Greedy: sort by end time<br/>• Select maximum non-overlapping"]
        
        Meeting["Meeting Rooms<br/>• Sort by start time<br/>• Use heap for end times"]
    end
    
    subgraph "General Strategy"
        Sort["1. Sort intervals (usually by start time)"]
        Process["2. Process in order"]
        Maintain["3. Maintain invariant (merged, non-overlapping, etc.)"]
        
        Sort --> Process --> Maintain
    end
```

### Tree Traversal Patterns

```mermaid
graph TB
    subgraph "Tree Traversal Strategies"
        DFS["Depth-First Search<br/>• Preorder: Root → Left → Right<br/>• Inorder: Left → Root → Right<br/>• Postorder: Left → Right → Root"]
        
        BFS["Breadth-First Search<br/>• Level-by-level traversal<br/>• Use queue for implementation"]
        
        Morris["Morris Traversal<br/>• O(1) space traversal<br/>• Modify tree temporarily"]
    end
    
    subgraph "Problem Pattern Matching"
        PathSum["Path Sum Problems → DFS"]
        LevelOrder["Level Order Problems → BFS"]
        Serialize["Serialize/Deserialize → Preorder DFS"]
        BST["BST Problems → Inorder DFS"]
        TreeDP["Tree DP → Postorder DFS"]
    end
```

## Interview Strategy Framework

### Problem-Solving Process

```mermaid
flowchart TD
    Start[Problem Statement] --> Understand[Understand Requirements]
    
    Understand --> Examples[Work Through Examples]
    Examples --> Edge[Consider Edge Cases]
    Edge --> Approach[Choose Approach]
    
    Approach --> BruteForce{Start with Brute Force?}
    BruteForce -->|Yes| Simple[Implement Simple Solution]
    BruteForce -->|No| Optimal[Design Optimal Solution]
    
    Simple --> Optimize[Optimize if Needed]
    Optimal --> Implement[Implement Solution]
    Optimize --> Implement
    
    Implement --> Test[Test with Examples]
    Test --> Debug{Issues Found?}
    
    Debug -->|Yes| Fix[Debug and Fix]
    Debug -->|No| Complexity[Analyze Complexity]
    
    Fix --> Test
    Complexity --> Discuss[Discuss Trade-offs]
```

### Communication Strategy

```mermaid
graph TB
    subgraph "Interview Communication"
        ThinkAloud["Think Aloud<br/>• Verbalize thought process<br/>• Explain approach selection<br/>• Discuss alternatives"]
        
        Clarify["Ask Clarifying Questions<br/>• Input constraints<br/>• Expected output format<br/>• Edge case handling"]
        
        Optimize["Discuss Optimizations<br/>• Time vs space tradeoffs<br/>• Different approaches<br/>• Scalability considerations"]
        
        Test["Testing Strategy<br/>• Walk through examples<br/>• Discuss edge cases<br/>• Explain debugging approach"]
    end
    
    subgraph "Red Flags to Avoid"
        Silent["Silent coding"]
        Stuck["Getting stuck without asking for help"]
        Defensive["Being defensive about approach"]
        Unclear["Unclear explanations"]
    end
```

## Complexity Cheat Sheet

### Quick Reference Table

| Operation | Best | Average | Worst |
|-----------|------|---------|-------|
| Array Access | O(1) | O(1) | O(1) |
| Array Search | O(1) | O(n) | O(n) |
| Array Insert | O(1) | O(n) | O(n) |
| Binary Search | O(1) | O(log n) | O(log n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Hash Table | O(1) | O(1) | O(n) |
| BST | O(log n) | O(log n) | O(n) |
| Heap Insert | O(1) | O(log n) | O(log n) |
| Graph BFS/DFS | O(V) | O(V+E) | O(V+E) |

### Master Theorem

```mermaid
graph TB
    subgraph "Master Theorem for Recurrence Relations"
        Form["T(n) = aT(n/b) + f(n)<br/>where a ≥ 1, b > 1"]
        
        Case1["Case 1: f(n) = O(n^(log_b(a) - ε))<br/>→ T(n) = Θ(n^log_b(a))"]
        
        Case2["Case 2: f(n) = Θ(n^log_b(a))<br/>→ T(n) = Θ(n^log_b(a) * log n)"]
        
        Case3["Case 3: f(n) = Ω(n^(log_b(a) + ε))<br/>→ T(n) = Θ(f(n))"]
        
        Examples["Examples:<br/>• Merge Sort: T(n) = 2T(n/2) + n → O(n log n)<br/>• Binary Search: T(n) = T(n/2) + 1 → O(log n)<br/>• Strassen: T(n) = 7T(n/2) + n² → O(n^2.81)"]
    end
```

## Key Takeaways

1. **Pattern Recognition**: Most interview problems fall into well-known patterns
2. **Constraint Analysis**: Input size determines acceptable time complexity
3. **Trade-offs**: Always consider time vs space trade-offs
4. **Communication**: Clear explanation is as important as correct solution
5. **Optimization**: Start simple, then optimize based on requirements
6. **Edge Cases**: Always consider boundary conditions and special cases

This framework provides a systematic approach to tackling technical interview problems across various domains and complexity levels.
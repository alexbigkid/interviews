# Array Algorithms - Visual Guide

This comprehensive guide provides visual representations of key array algorithms and patterns essential for technical interviews.

## Algorithm Categories Overview

```mermaid
graph TB
    A[Array Algorithms] --> B[Basic Operations]
    A --> C[Sorting & Searching]
    A --> D[Two Pointers]
    A --> E[Sliding Window]
    A --> F[Dynamic Programming]
    A --> G[Advanced Techniques]
    
    B --> B1[Array Traversal]
    B --> B2[Element Operations]
    B --> B3[Subarray Problems]
    
    C --> C1[Binary Search]
    C --> C2[Sorting Algorithms]
    C --> C3[Search Variations]
    
    D --> D1[Opposite Ends]
    D --> D2[Same Direction]
    D --> D3[Cycle Detection]
    
    E --> E1[Fixed Size]
    E --> E2[Variable Size]
    E --> E3[Multiple Windows]
    
    F --> F1[1D DP]
    F --> F2[2D DP]
    F --> F3[State Machines]
    
    G --> G1[Prefix/Suffix]
    G --> G2[Interval Problems]
    G --> G3[Matrix Operations]
```

## Complexity Analysis Reference

```mermaid
graph TB
    subgraph "Time Complexity Hierarchy"
        T1[O(1) - Direct Access]
        T2[O(log n) - Binary Search]
        T3[O(n) - Linear Scan]
        T4[O(n log n) - Efficient Sort]
        T5[O(n²) - Nested Loops]
        T6[O(n³) - Triple Nested]
        T7[O(2ⁿ) - Exponential]
        
        T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7
    end
    
    subgraph "Space Complexity"
        S1[O(1) - In-place]
        S2[O(log n) - Recursion Stack]
        S3[O(n) - Linear Space]
        S4[O(n²) - 2D Arrays]
    end
```

## Problem Pattern Recognition

```mermaid
flowchart TD
    Start([Array Problem]) --> Q1{Sorted Array?}
    
    Q1 -->|Yes| Q2{Search Problem?}
    Q1 -->|No| Q3{Need Sorting?}
    
    Q2 -->|Yes| BinarySearch[Binary Search Variants<br/>O(log n)]
    Q2 -->|No| Q4{Two Elements?}
    
    Q3 -->|Yes| SortFirst[Sort Then Process<br/>O(n log n)]
    Q3 -->|No| Q5{Subarray Problem?}
    
    Q4 -->|Yes| TwoPointers[Two Pointers<br/>O(n)]
    Q4 -->|No| Q6{All Subarrays?}
    
    Q5 -->|Yes| Q7{Fixed/Variable Size?}
    Q5 -->|No| Q8{Optimization Problem?}
    
    Q6 -->|Yes| NestedLoops[Nested Loops<br/>O(n²) or O(n³)]
    Q6 -->|No| Q9{Matrix Problem?}
    
    Q7 -->|Fixed| SlidingWindow[Sliding Window<br/>O(n)]
    Q7 -->|Variable| TwoPointersVar[Two Pointers/HashMap<br/>O(n)]
    
    Q8 -->|Yes| DP[Dynamic Programming<br/>Various complexity]
    Q8 -->|No| Greedy[Greedy Algorithm<br/>O(n) or O(n log n)]
    
    Q9 -->|Yes| Matrix[Matrix Algorithms<br/>O(m×n)]
    Q9 -->|No| Advanced[Advanced Techniques<br/>Problem-specific]
```

## Common Array Patterns

### 1. Two Pointers Pattern

```mermaid
graph TB
    subgraph "Two Pointers Variations"
        A["Opposite Ends<br/>Example: Two Sum in sorted array"]
        B["Same Direction<br/>Example: Remove duplicates"]
        C["Fast & Slow<br/>Example: Cycle detection"]
        
        A1["left=0, right=n-1<br/>Move based on condition"]
        B1["slow=0, fast=0<br/>Fast pointer scouts ahead"]
        C1["slow=head, fast=head<br/>Fast moves 2x speed"]
        
        A --> A1
        B --> B1
        C --> C1
    end
```

### 2. Sliding Window Pattern

```mermaid
graph LR
    subgraph "Sliding Window Types"
        Fixed["Fixed Size Window<br/>Example: Max sum of k elements"]
        Variable["Variable Size Window<br/>Example: Longest substring with k unique chars"]
        
        FixedAlgo["1. Calculate first window<br/>2. Slide by removing left, adding right<br/>3. Update result"]
        VarAlgo["1. Expand window with right pointer<br/>2. Contract with left when invalid<br/>3. Update result when valid"]
        
        Fixed --> FixedAlgo
        Variable --> VarAlgo
    end
```

### 3. Prefix/Suffix Pattern

```mermaid
graph TB
    subgraph "Prefix Sum Application"
        Array["Array: [1, 2, 3, 4, 5]"]
        Prefix["Prefix: [0, 1, 3, 6, 10, 15]"]
        Query["Range sum [i,j] = prefix[j+1] - prefix[i]"]
        
        Array --> Prefix --> Query
    end
    
    subgraph "Product Except Self"
        Left["Left products: [1, a[0], a[0]*a[1], ...]"]
        Right["Right products: [..., a[n-2]*a[n-1], a[n-1], 1]"]
        Result["result[i] = left[i] * right[i]"]
        
        Left --> Result
        Right --> Result
    end
```

## Algorithm Visualizations

### Binary Search Variants

```mermaid
graph TB
    subgraph "Binary Search Template"
        Template["
        while left <= right:
            mid = left + (right - left) // 2
            if condition(mid):
                right = mid - 1  # search left
            else:
                left = mid + 1   # search right
        return answer
        "]
    end
    
    subgraph "Search Variations"
        Exact["Find exact target"]
        FirstOccur["Find first occurrence"]
        LastOccur["Find last occurrence"]
        Ceiling["Find ceiling (smallest >= target)"]
        Floor["Find floor (largest <= target)"]
        Peak["Find peak element"]
        Rotated["Search in rotated sorted array"]
    end
```

### Merge Intervals Algorithm

```mermaid
sequenceDiagram
    participant S as Sorted Intervals
    participant R as Result
    participant C as Current
    
    Note over S: [[1,3], [2,6], [8,10], [15,18]]
    
    S->>R: Add [1,3] to result
    S->>C: Process [2,6]
    
    Note over C: 2 <= 3, overlaps with [1,3]
    C->>R: Merge to [1,6]
    
    S->>C: Process [8,10]
    Note over C: 8 > 6, no overlap
    C->>R: Add [8,10] to result
    
    S->>C: Process [15,18]
    Note over C: 15 > 10, no overlap
    C->>R: Add [15,18] to result
    
    Note over R: Final: [[1,6], [8,10], [15,18]]
```

### Kadane's Algorithm (Maximum Subarray)

```mermaid
graph LR
    subgraph "Kadane's Algorithm Visualization"
        A["Array: [-2, 1, -3, 4, -1, 2, 1, -5, 4]"]
        
        Step1["current_sum = -2, max_sum = -2"]
        Step2["current_sum = 1, max_sum = 1"]
        Step3["current_sum = -2, max_sum = 1"]
        Step4["current_sum = 4, max_sum = 4"]
        Step5["current_sum = 3, max_sum = 4"]
        Step6["current_sum = 5, max_sum = 5"]
        Step7["current_sum = 6, max_sum = 6"]
        
        Rule["If current_sum < 0: reset to 0<br/>Always update max_sum"]
    end
```

## Dynamic Programming on Arrays

### 1D DP Patterns

```mermaid
graph TB
    subgraph "Common 1D DP Problems"
        Climb["Climbing Stairs<br/>dp[i] = dp[i-1] + dp[i-2]"]
        House["House Robber<br/>dp[i] = max(dp[i-1], dp[i-2] + nums[i])"]
        Jump["Jump Game<br/>dp[i] = can reach position i"]
        Coin["Coin Change<br/>dp[i] = min coins for amount i"]
        
        Pattern["Pattern: Current state depends on<br/>previous states with simple recurrence"]
    end
```

### 2D DP Patterns

```mermaid
graph TB
    subgraph "2D DP Problems"
        Grid["Unique Paths<br/>dp[i][j] = dp[i-1][j] + dp[i][j-1]"]
        MinPath["Minimum Path Sum<br/>dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]"]
        LIS["Longest Increasing Subsequence<br/>dp[i] = max length ending at i"]
        Edit["Edit Distance<br/>dp[i][j] = min operations to transform"]
    end
```

## Matrix Algorithms

### Matrix Traversal Patterns

```mermaid
graph TB
    subgraph "Matrix Traversal Types"
        Spiral["Spiral Traversal<br/>Outside → Inside"]
        Diagonal["Diagonal Traversal<br/>Main/Anti diagonals"]
        Layer["Layer-by-layer<br/>Process outer layers first"]
        DFS["DFS/BFS Traversal<br/>For connected components"]
    end
    
    subgraph "Spiral Direction Management"
        Directions["Right → Down → Left → Up → Repeat"]
        Boundaries["Track: top, bottom, left, right boundaries"]
        Update["Update boundaries after each direction"]
    end
```

### Matrix Rotation and Transformation

```mermaid
graph LR
    subgraph "90° Clockwise Rotation"
        Original["
        1 2 3
        4 5 6
        7 8 9
        "]
        
        Step1["Transpose:<br/>
        1 4 7
        2 5 8
        3 6 9
        "]
        
        Step2["Reverse rows:<br/>
        7 4 1
        8 5 2
        9 6 3
        "]
        
        Original --> Step1 --> Step2
    end
```

## Advanced Array Techniques

### Union-Find for Array Problems

```mermaid
graph TB
    subgraph "Union-Find Applications"
        Islands["Number of Islands<br/>Union adjacent land cells"]
        Components["Connected Components<br/>Track disjoint sets"]
        Percolation["Percolation Problems<br/>Path existence checks"]
        
        Operations["Union(x,y): Connect elements<br/>Find(x): Get root representative<br/>Connected(x,y): Same component?"]
    end
```

### Monotonic Stack/Queue

```mermaid
graph TB
    subgraph "Monotonic Stack Applications"
        NextGreater["Next Greater Element<br/>Maintain decreasing stack"]
        Histogram["Largest Rectangle<br/>Stack of indices"]
        Temperature["Daily Temperatures<br/>Stack for waiting days"]
        
        Property["Property: Stack maintains<br/>monotonic order (increasing/decreasing)"]
    end
    
    subgraph "Algorithm Pattern"
        Process["
        For each element:
        1. Pop stack while condition violated
        2. Process current element with stack top
        3. Push current element to stack
        "]
    end
```

## Problem Complexity Guide

```mermaid
graph TB
    subgraph "Array Problem Complexity Guide"
        Simple["O(n) - Single pass, two pointers, sliding window"]
        Medium["O(n log n) - Sorting-based, binary search variations"]
        Complex["O(n²) - Nested loops, some DP problems"]
        Advanced["O(n³) or higher - Matrix multiplication, complex DP"]
        
        Optimal["Space optimization often possible:<br/>O(n) → O(1) for many problems"]
    end
```

## Strategy Selection Framework

```mermaid
flowchart TD
    Problem[Array Problem] --> Constraints{Check Constraints}
    
    Constraints -->|n ≤ 100| Quadratic[O(n²) solutions acceptable]
    Constraints -->|n ≤ 10⁵| Linear[O(n) or O(n log n) needed]
    Constraints -->|n ≤ 10⁶| StrictLinear[O(n) or better required]
    
    Quadratic --> BruteForce[Consider brute force first]
    Linear --> Optimize[Look for patterns/sorting]
    StrictLinear --> Advanced[Advanced techniques needed]
    
    BruteForce --> Correct{Correct solution?}
    Optimize --> Efficient{Efficient enough?}
    Advanced --> Feasible{Feasible approach?}
    
    Correct -->|Yes| Optimize2[Then optimize if needed]
    Efficient -->|Yes| Implement[Implement solution]
    Feasible -->|Yes| Implement
    
    Correct -->|No| Debug[Debug approach]
    Efficient -->|No| Rethink[Rethink algorithm]
    Feasible -->|No| Research[Research advanced techniques]
```

## Next Steps

- [Basic Array Operations](basic-operations.md)
- [Sorting and Searching](sorting-searching.md)
- [Two Pointers and Sliding Window](two-pointers-sliding-window.md)
- [Dynamic Programming on Arrays](dynamic-programming.md)
- [Advanced Array Techniques](advanced-techniques.md)

## Quick Reference Card

| Problem Type | Algorithm | Time | Space | Key Insight |
|--------------|-----------|------|-------|-------------|
| Two Sum | HashMap | O(n) | O(n) | Store complement |
| Subarray Sum | Prefix Sum | O(n) | O(1) | Cumulative sums |
| Sliding Window | Two Pointers | O(n) | O(1) | Expand/contract |
| Binary Search | Divide & Conquer | O(log n) | O(1) | Eliminate half |
| Merge Intervals | Sorting | O(n log n) | O(1) | Sort by start time |
| Matrix Spiral | Boundary Tracking | O(m×n) | O(1) | Direction management |
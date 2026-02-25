# Basic Array Operations - Visual Guide

This guide covers fundamental array operations with comprehensive visualizations and complexity analysis.

## Array Access and Manipulation

### Random Access Visualization

```mermaid
graph LR
    subgraph "Array Memory Layout"
        A["Index: 0 1 2 3 4"]
        B["Value: 5 3 8 1 9"]
        C["Addr:  100 104 108 112 116"]
        
        D["Direct access: arr[3] = address(arr) + 3 * sizeof(int)"]
    end
    
    subgraph "Time Complexity"
        Access["Access: O(1)"]
        Insert["Insert at end: O(1)"]
        InsertMiddle["Insert at middle: O(n)"]
        Delete["Delete: O(n)"]
        Search["Search: O(n)"]
    end
```

## Two Sum Problem Patterns

### Brute Force Approach

```mermaid
sequenceDiagram
    participant A as Array [2,7,11,15]
    participant T as Target: 9
    participant R as Result
    
    Note over A,R: Nested loop approach
    A->>A: i=0, j=1: 2+7=9 ✓
    A->>R: Return [0,1]
    
    Note over A,R: Time: O(n²), Space: O(1)
```

### HashMap Optimization

```mermaid
graph TB
    subgraph "HashMap Two Sum"
        Step1["For each number in array"]
        Step2["Calculate complement = target - number"]
        Step3["Check if complement in hashmap"]
        Step4["If yes: return indices"]
        Step5["If no: store number with index"]
        
        Step1 --> Step2 --> Step3 --> Step4
        Step3 --> Step5 --> Step1
    end
    
    subgraph "Example: [2,7,11,15], target=9"
        Ex1["num=2, complement=7, map={}, store 2→0"]
        Ex2["num=7, complement=2, map={2:0}, found! return [0,1]"]
        
        Ex1 --> Ex2
    end
```

## Three Sum Problem

### Sorting + Two Pointers Approach

```mermaid
graph TB
    subgraph "Three Sum Algorithm"
        Sort["1. Sort array: O(n log n)"]
        Outer["2. For each element (outer loop)"]
        Skip["3. Skip duplicates for outer element"]
        TwoPointer["4. Use two pointers for remaining array"]
        Check["5. Check sum of three elements"]
        Adjust["6. Adjust pointers based on sum"]
        
        Sort --> Outer --> Skip --> TwoPointer --> Check --> Adjust --> TwoPointer
    end
```

### Visual Example: [-1,0,1,2,-1,-4]

```mermaid
sequenceDiagram
    participant Sorted as [-4,-1,-1,0,1,2]
    participant i as Outer Index
    participant L as Left Pointer  
    participant R as Right Pointer
    
    Note over Sorted: i=1 (value=-1), L=2, R=5
    Sorted->>i: nums[1] = -1
    Sorted->>L: nums[2] = -1  
    Sorted->>R: nums[5] = 2
    
    Note over Sorted: Sum = -1 + (-1) + 2 = 0 ✓
    Note over Sorted: Found triplet: [-1,-1,2]
    
    Note over Sorted: Move L right, R left, skip duplicates
    L->>L: L = 3 (value=0)
    R->>R: R = 4 (value=1)
    
    Note over Sorted: Sum = -1 + 0 + 1 = 0 ✓  
    Note over Sorted: Found triplet: [-1,0,1]
```

## Container With Most Water

### Two Pointers Strategy

```mermaid
graph TB
    subgraph "Water Container Visualization"
        Array["Heights: [1,8,6,2,5,4,8,3,7]"]
        Initial["left=0 (height=1), right=8 (height=7)"]
        Area1["Area = min(1,7) × (8-0) = 8"]
        
        Move1["Move left++ (shorter line)"]
        State2["left=1 (height=8), right=8 (height=7)"]
        Area2["Area = min(8,7) × (8-1) = 49"]
        
        Array --> Initial --> Area1 --> Move1 --> State2 --> Area2
    end
    
    subgraph "Algorithm Logic"
        Rule["Always move pointer with shorter height"]
        Reason["Moving taller pointer can't increase area<br/>(width decreases, height limited by shorter)"]
        Optimal["This guarantees we find maximum area"]
        
        Rule --> Reason --> Optimal
    end
```

## Sliding Window Maximum

### Deque-Based Solution

```mermaid
graph TB
    subgraph "Sliding Window Maximum with Deque"
        Array["Array: [1,3,-1,-3,5,3,6,7], k=3"]
        
        Window1["Window [1,3,-1]: max=3<br/>Deque: [3] (store indices)"]
        Window2["Window [3,-1,-3]: max=3<br/>Deque: [3]"]
        Window3["Window [-1,-3,5]: max=5<br/>Deque: [5]"]
        Window4["Window [-3,5,3]: max=5<br/>Deque: [5,3]"]
        
        Array --> Window1 --> Window2 --> Window3 --> Window4
    end
    
    subgraph "Deque Operations"
        Add["Adding element:<br/>1. Remove elements smaller than current<br/>2. Add current to back"]
        Remove["Removing element:<br/>1. Check if front is out of window<br/>2. Remove if necessary"]
        Query["Get maximum:<br/>Front of deque is always maximum"]
        
        Complexity["Time: O(n), Space: O(k)"]
    end
```

## Array Rotation

### Reversal Algorithm

```mermaid
graph TB
    subgraph "Rotate Array Left by k=3"
        Original["[1,2,3,4,5,6,7] → rotate left by 3"]
        
        Step1["Reverse entire array:<br/>[7,6,5,4,3,2,1]"]
        Step2["Reverse first (n-k) elements:<br/>[4,5,6,7,3,2,1]"]
        Step3["Reverse last k elements:<br/>[4,5,6,7,1,2,3]"]
        
        Original --> Step1 --> Step2 --> Step3
    end
    
    subgraph "Alternative: Cyclic Replacement"
        Cycle["Place each element directly<br/>at its final position"]
        GCD["Number of cycles = gcd(n,k)"]
        Efficient["Time: O(n), Space: O(1)"]
        
        Cycle --> GCD --> Efficient
    end
```

## Kadane's Algorithm (Maximum Subarray)

### Algorithm Visualization

```mermaid
graph TB
    subgraph "Kadane's Algorithm Step-by-Step"
        Array["[-2,1,-3,4,-1,2,1,-5,4]"]
        
        Init["current_sum = 0, max_sum = -∞"]
        
        S1["i=0: current_sum = max(0-2, -2) = -2, max_sum = -2"]
        S2["i=1: current_sum = max(-2+1, 1) = 1, max_sum = 1"]
        S3["i=2: current_sum = max(1-3, -3) = -2, max_sum = 1"]
        S4["i=3: current_sum = max(-2+4, 4) = 4, max_sum = 4"]
        S5["i=4: current_sum = max(4-1, -1) = 3, max_sum = 4"]
        S6["i=5: current_sum = max(3+2, 2) = 5, max_sum = 5"]
        S7["i=6: current_sum = max(5+1, 1) = 6, max_sum = 6"]
        
        Array --> Init --> S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
    end
    
    subgraph "Key Insight"
        Insight["If current_sum becomes negative,<br/>start fresh (reset to 0)<br/>Negative prefix can only hurt"]
    end
```

## Stock Trading Problems

### Single Transaction

```mermaid
graph LR
    subgraph "Best Time to Buy and Sell Stock"
        Prices["[7,1,5,3,6,4]"]
        
        Track["Track minimum price seen so far"]
        Profit["Calculate profit if selling today"]
        Update["Update maximum profit"]
        
        Track --> Profit --> Update
    end
    
    subgraph "State Tracking"
        MinPrice["min_price = min(min_price, price[i])"]
        MaxProfit["max_profit = max(max_profit, price[i] - min_price)"]
        
        Example["Day 0: min=7, profit=0<br/>Day 1: min=1, profit=0<br/>Day 2: min=1, profit=4<br/>Day 3: min=1, profit=4<br/>Day 4: min=1, profit=5"]
    end
```

### Multiple Transactions

```mermaid
graph TB
    subgraph "Multiple Transactions Strategy"
        Greedy["Greedy: Buy before every price increase,<br/>sell before every price decrease"]
        
        Example["Prices: [1,5,3,6,4]<br/>Buy at 1, sell at 5: profit = 4<br/>Buy at 3, sell at 6: profit = 3<br/>Total profit = 7"]
        
        Implementation["For each day:<br/>if price[i] > price[i-1]:<br/>    profit += price[i] - price[i-1]"]
        
        Greedy --> Example --> Implementation
    end
```

## Dutch Flag Problem (Sort Colors)

### Three-Way Partitioning

```mermaid
graph TB
    subgraph "Dutch Flag Algorithm"
        Array["[2,0,2,1,1,0] - Sort 0s, 1s, 2s"]
        
        Pointers["low=0 (next position for 0)<br/>mid=0 (current element)<br/>high=5 (next position for 2)"]
        
        Rules["
        If nums[mid] == 0: swap with low, increment low and mid
        If nums[mid] == 1: increment mid only  
        If nums[mid] == 2: swap with high, decrement high (don't increment mid)
        "]
        
        Array --> Pointers --> Rules
    end
    
    subgraph "Invariants"
        Inv1["[0...low-1] contains all 0s"]
        Inv2["[low...mid-1] contains all 1s"]
        Inv3["[high+1...n-1] contains all 2s"]
        Inv4["[mid...high] contains unprocessed elements"]
    end
```

## Product of Array Except Self

### Two-Pass Solution

```mermaid
graph TB
    subgraph "Product Except Self Algorithm"
        Input["Input: [1,2,3,4]"]
        
        LeftPass["Left pass - products of elements to the left:"]
        LeftResult["[1, 1, 1×2, 1×2×3] = [1,1,2,6]"]
        
        RightPass["Right pass - multiply by products from right:"]
        RightCalc["
        result[3] = 6 × 1 = 6 (no elements to right)
        result[2] = 2 × 4 = 8 (4 to right)  
        result[1] = 1 × 4×3 = 12 (3,4 to right)
        result[0] = 1 × 4×3×2 = 24 (2,3,4 to right)
        "]
        
        Input --> LeftPass --> LeftResult --> RightPass --> RightCalc
    end
    
    subgraph "Space Optimization"
        Opt["Use result array for left products,<br/>then multiply by right products in-place<br/>Space: O(1) extra"]
    end
```

## First Missing Positive

### Cyclic Sort Approach

```mermaid
graph TB
    subgraph "First Missing Positive Algorithm"
        Idea["Place each positive number n at index n-1<br/>if it's within bounds [1, length]"]
        
        Input["[3,4,-1,1]"]
        
        Step1["Place 3 at index 2: [3,4,-1,1] → [-1,4,3,1]"]
        Step2["Place 4 at index 3: [-1,4,3,1] → [-1,1,3,4]"]
        Step3["Place 1 at index 0: [-1,1,3,4] → [1,-1,3,4]"]
        
        Find["First index i where nums[i] != i+1<br/>Answer: i+1 (or length+1 if all present)"]
        
        Input --> Step1 --> Step2 --> Step3 --> Find
    end
    
    subgraph "Key Insights"
        Insight1["Only care about numbers in range [1,n]"]
        Insight2["Use array indices as hash positions"]
        Insight3["First missing must be in range [1,n+1]"]
    end
```

## Trapping Rain Water

### Two Pointers Solution

```mermaid
graph TB
    subgraph "Rain Water Trapping"
        Heights["Heights: [0,1,0,2,1,0,1,3,2,1,2,1]"]
        
        Concept["Water at position i = min(max_left, max_right) - height[i]"]
        
        TwoPointer["Use two pointers from both ends<br/>Move pointer with smaller max height"]
        
        Logic["
        If left_max < right_max:
            water += left_max - height[left]
            move left pointer right
        Else:
            water += right_max - height[right]  
            move right pointer left
        "]
        
        Heights --> Concept --> TwoPointer --> Logic
    end
    
    subgraph "Visualization"
        Visual["
        |   |   | ■ |   |   |   |   | ■ |   |   |   |   |
        |   | ■ | ~ | ■ |   |   | ■ | ■ | ■ |   | ■ |   |
        |   | ■ | ~ | ■ | ■ | ~ | ■ | ■ | ■ | ■ | ■ | ■ |
        
        ■ = walls, ~ = trapped water
        "]
    end
```

## Performance Comparison Table

```mermaid
graph TB
    subgraph "Algorithm Complexity Summary"
        A["Two Sum: O(n) time, O(n) space (HashMap)"]
        B["Three Sum: O(n²) time, O(1) space"]
        C["Container Water: O(n) time, O(1) space"]
        D["Sliding Window Max: O(n) time, O(k) space"]
        E["Array Rotation: O(n) time, O(1) space"]
        F["Maximum Subarray: O(n) time, O(1) space"]
        G["Stock Trading: O(n) time, O(1) space"]
        H["Sort Colors: O(n) time, O(1) space"]
        I["Product Except Self: O(n) time, O(1) space"]
        J["First Missing Positive: O(n) time, O(1) space"]
        K["Trapping Rain Water: O(n) time, O(1) space"]
    end
```

## Problem-Solving Strategy

```mermaid
flowchart TD
    Problem[Array Problem] --> Analyze{Analyze Requirements}
    
    Analyze -->|Need all pairs| PairProblems[Consider O(n²) approaches<br/>or HashMap optimization]
    Analyze -->|Subarray problem| Subarray[Sliding window or<br/>prefix sum techniques]
    Analyze -->|Sorted array| Sorted[Binary search or<br/>two pointers]
    Analyze -->|Optimization| DP[Dynamic programming<br/>or greedy approach]
    
    PairProblems --> TwoSum[Two Sum variants]
    Subarray --> MaxSubarray[Maximum subarray,<br/>sliding window maximum]
    Sorted --> BinarySearch[Search problems,<br/>merge operations]
    DP --> OptimalSolution[Kadane's algorithm,<br/>stock trading]
    
    Optimize["Always consider:<br/>1. Can we do it in one pass?<br/>2. Can we use O(1) extra space?<br/>3. Can we avoid sorting?"]
```

## Key Insights

1. **Array as HashMap**: Use array indices as hash keys when elements are in known range
2. **Two Pointers**: Powerful for sorted arrays and optimization problems  
3. **Sliding Window**: Essential for subarray problems with constraints
4. **In-place Operations**: Many problems can be solved without extra space
5. **Preprocessing**: Sometimes sorting or prefix computation enables efficient queries
6. **Invariant Maintenance**: Keep track of what each section of array represents

## Next: [Sorting and Searching Algorithms →](sorting-searching.md)
# String Algorithms - Visual Guide

This comprehensive guide provides visual representations of key string algorithms and patterns commonly encountered in technical interviews.

## Algorithm Categories Overview

```mermaid
graph TB
    A[String Algorithms] --> B[Basic Operations]
    A --> C[Pattern Matching]
    A --> D[Dynamic Programming]
    A --> E[Transformations]
    A --> F[Advanced Problems]
    
    B --> B1[Character Frequency]
    B --> B2[String Reversal]
    B --> B3[Subsequences]
    
    C --> C1[KMP Algorithm]
    C --> C2[Rabin-Karp]
    C --> C3[Boyer-Moore]
    C --> C4[Z-Algorithm]
    
    D --> D1[Edit Distance]
    D --> D2[LCS/LIS]
    D --> D3[Palindromes]
    D --> D4[Word Break]
    
    E --> E1[Case Conversion]
    E --> E2[Compression]
    E --> E3[Encoding/Decoding]
    E --> E4[Cipher Operations]
    
    F --> F1[Anagrams]
    F --> F2[String Matching]
    F --> F3[Substring Problems]
    F --> F4[Advanced DP]
```

## Complexity Analysis Reference

```mermaid
graph LR
    subgraph "Time Complexity"
        A1[O(1) - Character Access]
        A2[O(n) - Linear Scan]
        A3[O(n log n) - Sorting Based]
        A4[O(n²) - Nested Loops]
        A5[O(n³) - Triple Nested]
    end
    
    subgraph "Space Complexity"
        B1[O(1) - In-place]
        B2[O(n) - Linear Space]
        B3[O(n²) - 2D Arrays]
        B4[O(k) - Dictionary Size]
    end
```

## Pattern Recognition Flowchart

```mermaid
flowchart TD
    Start([Problem Statement]) --> Q1{String Comparison?}
    
    Q1 -->|Yes| Q2{Exact Match?}
    Q1 -->|No| Q3{Character Analysis?}
    
    Q2 -->|Yes| Pattern1[String Equality<br/>KMP, Rabin-Karp]
    Q2 -->|No| Q4{Substring Search?}
    
    Q3 -->|Yes| Q5{Frequency Count?}
    Q3 -->|No| Q6{Transformation?}
    
    Q4 -->|Yes| Pattern2[Pattern Matching<br/>Boyer-Moore, Z-Algorithm]
    Q4 -->|No| Q7{Similarity Measure?}
    
    Q5 -->|Yes| Pattern3[HashMap/Array<br/>Character Frequency]
    Q5 -->|No| Q8{Order Matters?}
    
    Q6 -->|Yes| Pattern4[String Manipulation<br/>Case, Reverse, etc.]
    Q6 -->|No| Q9{Optimization Problem?}
    
    Q7 -->|Yes| Pattern5[Dynamic Programming<br/>Edit Distance, LCS]
    Q8 -->|Yes| Pattern6[Subsequence<br/>Two Pointers, DP]
    Q8 -->|No| Pattern7[Anagram Detection<br/>Sorting, HashMap]
    
    Q9 -->|Yes| Pattern8[Advanced DP<br/>Word Break, Palindromes]
    Q9 -->|No| Pattern9[Greedy/Other<br/>Custom Logic]
```

## Common String Patterns

### 1. Two Pointers Pattern
Used for: Palindrome checking, subsequence validation, in-place operations

```mermaid
graph LR
    subgraph "String: 'racecar'"
        A[r] --- B[a] --- C[c] --- D[e] --- E[c] --- F[a] --- G[r]
    end
    
    L[Left Pointer] -.-> A
    R[Right Pointer] -.-> G
    
    Step1[Compare chars] --> Step2[Move pointers inward]
    Step2 --> Step3[Continue until meet]
```

### 2. Sliding Window Pattern
Used for: Minimum window substring, longest substring problems

```mermaid
graph TB
    subgraph "String: 'ADOBECODEBANC'"
        S[A|D|O|B|E|C|O|D|E|B|A|N|C]
    end
    
    W1[Window 1: ADO] --> W2[Window 2: DOBA]
    W2 --> W3[Window 3: BANC ✓]
    
    Note[Expand right until valid<br/>Contract left while valid]
```

### 3. Dynamic Programming Pattern
Used for: Edit distance, longest common subsequence, palindrome problems

```mermaid
graph TB
    subgraph "DP Table Example: Edit Distance"
        direction TB
        T1[" |ε|h|o|r|s|e"]
        T2["ε|0|1|2|3|4|5"]
        T3["r|1|1|2|2|3|4"]
        T4["o|2|2|1|2|3|4"]
        T5["s|3|3|2|2|2|3"]
    end
    
    Formula["dp[i][j] = min(<br/>dp[i-1][j] + 1,<br/>dp[i][j-1] + 1,<br/>dp[i-1][j-1] + cost)"]
```

## Algorithm Visualization Examples

### KMP Algorithm Pattern Matching

```mermaid
flowchart TD
    subgraph "KMP Failure Function"
        P["Pattern: ABCABCD"]
        F["Failure: [0,0,0,1,2,3,0]"]
    end
    
    subgraph "Matching Process"
        T["Text: ABCABCABCABCD"]
        M1["Match at position 6"] 
    end
    
    Process["1. Build failure function<br/>2. Use failure function to skip<br/>3. Continue matching"]
```

### Rabin-Karp Rolling Hash

```mermaid
graph LR
    subgraph "Rolling Hash Concept"
        H1["hash('ABC') = h1"] --> H2["hash('BCD') = (h1-A)*base + D"]
        H2 --> H3["Continue rolling..."]
    end
    
    subgraph "Pattern Detection"
        Compare["If hash matches<br/>→ Character-by-character check"]
    end
```

## Problem-Solving Strategies

### Strategy Selection Guide

```mermaid
flowchart TD
    Problem[String Problem] --> Size{String Size?}
    
    Size -->|Small n≤100| BruteForce[Brute Force O(n²)]
    Size -->|Medium n≤10⁴| Optimized[Optimized O(n log n)]
    Size -->|Large n≤10⁶| Linear[Linear O(n)]
    
    BruteForce --> Check1{Correctness First?}
    Optimized --> Check2{Pattern Matching?}
    Linear --> Check3{Single Pass Possible?}
    
    Check1 -->|Yes| Implement1[Simple Nested Loops]
    Check2 -->|Yes| Implement2[KMP/Rabin-Karp]
    Check3 -->|Yes| Implement3[Two Pointers/Sliding Window]
    
    Check1 -->|No| Optimize1[Think DP/Greedy]
    Check2 -->|No| Optimize2[HashMap/Sorting]
    Check3 -->|No| Optimize3[Advanced Data Structures]
```

### Time vs Space Trade-offs

```mermaid
graph TB
    subgraph "Trade-off Decisions"
        A[Preprocessing Time] --> B[Query Time]
        C[Memory Usage] --> D[Algorithm Choice]
        
        E["High Memory → Fast Queries<br/>(DP tables, preprocessing)"]
        F["Low Memory → Slower Queries<br/>(On-demand computation)"]
    end
    
    Examples["Examples:<br/>• Suffix Arrays: O(n) space, O(log n) search<br/>• KMP: O(m) space, O(n+m) time<br/>• Brute Force: O(1) space, O(nm) time"]
```

## Next Steps

- [Basic String Operations](basic-operations.md)
- [Pattern Matching Algorithms](pattern-matching.md)
- [Dynamic Programming on Strings](dynamic-programming.md)
- [Advanced String Problems](advanced-problems.md)

## Quick Reference

| Problem Type | Best Algorithm | Time | Space |
|--------------|----------------|------|-------|
| Exact Pattern Match | KMP | O(n+m) | O(m) |
| Multiple Pattern Search | Aho-Corasick | O(n+z) | O(total pattern length) |
| Edit Distance | DP | O(nm) | O(n) |
| Longest Palindrome | Expand Around Centers | O(n²) | O(1) |
| Anagram Check | Sorting/HashMap | O(n log n)/O(n) | O(1)/O(k) |
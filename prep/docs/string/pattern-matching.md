# Pattern Matching Algorithms - Visual Guide

This guide provides comprehensive visualizations of string pattern matching algorithms essential for technical interviews.

## Algorithm Overview and Selection

```mermaid
graph TB
    subgraph "Pattern Matching Algorithms"
        A[Input Requirements] --> B{Pattern Length}
        
        B -->|Short m<100| C[Brute Force O(nm)]
        B -->|Medium m<1000| D[KMP O(n+m)]
        B -->|Multiple patterns| E[Aho-Corasick]
        
        A --> F{Text Length}
        F -->|Large n>10⁶| G[Boyer-Moore]
        F -->|Rolling hash| H[Rabin-Karp]
        
        A --> I{Pattern Type}
        I -->|Exact match| J[KMP/Boyer-Moore]
        I -->|Wildcards| K[Dynamic Programming]
        I -->|Regular expressions| L[Finite Automaton]
    end
```

## Brute Force Algorithm

### Step-by-Step Visualization

```mermaid
sequenceDiagram
    participant T as Text: "ABABCABABA"
    participant P as Pattern: "ABAB"
    
    Note over T,P: Position 0
    T->>P: A matches A ✓
    T->>P: B matches B ✓  
    T->>P: A matches A ✓
    T->>P: B matches B ✓
    Note over T,P: Match found at position 0!
    
    Note over T,P: Continue search at position 1
    T->>P: B ≠ A ✗
    Note over T,P: Mismatch, move to position 2
    
    Note over T,P: Position 2
    T->>P: A matches A ✓
    T->>P: B matches B ✓
    T->>P: C ≠ A ✗
    Note over T,P: Mismatch, move to position 3
```

```mermaid
graph LR
    subgraph "Brute Force Complexity"
        A["Best case: O(n)<br/>Pattern found immediately"]
        B["Average case: O(nm)<br/>Multiple mismatches"]
        C["Worst case: O(nm)<br/>Pattern like 'aaa...ab' in 'aaa...aaa'"]
    end
```

## KMP (Knuth-Morris-Pratt) Algorithm

### Failure Function Construction

```mermaid
graph TB
    subgraph "Building Failure Function for 'ABCABCD'"
        Pattern["A B C A B C D"]
        Indices["0 1 2 3 4 5 6"]
        
        subgraph "Step-by-step"
            S1["Position 0: failure[0] = 0 (by definition)"]
            S2["Position 1: 'B' ≠ 'A', failure[1] = 0"]
            S3["Position 2: 'C' ≠ 'A', failure[2] = 0"] 
            S4["Position 3: 'A' = 'A', failure[3] = 1"]
            S5["Position 4: 'B' = 'B', failure[4] = 2"]
            S6["Position 5: 'C' = 'C', failure[5] = 3"]
            S7["Position 6: 'D' ≠ 'A', failure[6] = 0"]
        end
        
        Result["failure = [0, 0, 0, 1, 2, 3, 0]"]
    end
```

### Pattern Matching with KMP

```mermaid
sequenceDiagram
    participant T as Text: "ABCABCABCABCD"
    participant P as Pattern: "ABCABCD"
    participant F as Failure: "[0,0,0,1,2,3,0]"
    
    Note over T,P,F: Start matching
    loop Character comparison
        T->>P: Compare characters
        alt Match
            P->>F: Continue to next position
        else Mismatch
            P->>F: Use failure function to skip
            Note over T,P,F: Don't restart from beginning
        end
    end
    
    Note over T,P,F: Pattern found at position 6
```

### KMP Visualization with Mismatches

```mermaid
graph TB
    subgraph "KMP Advantage: Smart Skipping"
        Scenario["Text: ABABCABABA<br/>Pattern: ABABA<br/>Failure: [0,0,1,2,0]"]
        
        Step1["Position 0-2: ABA matches"]
        Step2["Position 3: B ≠ C, mismatch"]
        Step3["Use failure[2] = 1: skip to position 1"]
        Step4["Continue from partial match AB..."]
        
        Step1 --> Step2 --> Step3 --> Step4
    end
    
    Benefit["Benefit: Never re-examine<br/>previously matched characters"]
```

## Boyer-Moore Algorithm

### Bad Character Rule

```mermaid
graph LR
    subgraph "Bad Character Heuristic"
        Text["T E X T  S E A R C H"]
        Pattern["S E A R C H"]
        
        Align1["Initial alignment"]
        Mismatch["T ≠ S: bad character"]
        Shift["Shift pattern right<br/>to align T with T in pattern<br/>or skip if T not in pattern"]
        
        Align1 --> Mismatch --> Shift
    end
```

### Good Suffix Rule

```mermaid
graph TB
    subgraph "Good Suffix Heuristic"
        Example["Pattern: ABCDEFG<br/>Text:    ...XYZABCDEFQ"]
        
        Observation["Suffix 'ABCDEF' matches<br/>but G ≠ Q at position 6"]
        
        Strategy["Look for another occurrence<br/>of suffix 'ABCDEF' in pattern<br/>or longest prefix that matches<br/>a suffix of the good suffix"]
        
        Observation --> Strategy
    end
```

### Boyer-Moore Performance

```mermaid
graph LR
    subgraph "Boyer-Moore Complexity"
        Best["Best case: O(n/m)<br/>Skip entire pattern length"]
        Avg["Average case: O(n)<br/>Sublinear performance"]
        Worst["Worst case: O(nm)<br/>Degenerate patterns"]
    end
    
    Ideal["Ideal for: Large alphabets,<br/>long patterns, text search"]
```

## Rabin-Karp Algorithm

### Rolling Hash Concept

```mermaid
graph TB
    subgraph "Rolling Hash for Pattern 'ABC'"
        Hash1["hash('ABC') = 1×256² + 2×256¹ + 3×256⁰"]
        Hash2["hash('BCD') = 2×256² + 3×256¹ + 4×256⁰"]
        
        Formula["New hash = (old_hash - first_char×256^(m-1)) × 256 + new_char"]
        
        Hash1 --> Formula --> Hash2
    end
    
    subgraph "Algorithm Steps"
        Step1["1. Compute pattern hash"]
        Step2["2. Compute text window hash"]
        Step3["3. Compare hashes"]
        Step4["4. If equal, verify character by character"]
        Step5["5. Roll hash to next position"]
        
        Step1 --> Step2 --> Step3 --> Step4 --> Step5 --> Step3
    end
```

### Hash Collision Handling

```mermaid
flowchart TD
    HashMatch{Hash Values Equal?} 
    --> |Yes| CharCheck[Character-by-character verification]
    --> |Match| Found[Pattern Found!]
    --> |No Match| Continue[Continue Rolling]
    
    HashMatch --> |No| Continue
    Continue --> NextPos[Move to next position]
    NextPos --> HashMatch
    
    SpuriousHit["Spurious Hit:<br/>Same hash, different strings<br/>Example: 'AB' and 'BA' might hash same"]
```

## Z-Algorithm

### Z-Array Construction

```mermaid
graph TB
    subgraph "Z-Algorithm for 'ABCABCABC'"
        String["A B C A B C A B C"]
        Index[" 0 1 2 3 4 5 6 7 8"]
        ZArray["0 0 0 3 0 0 3 0 0"]
        
        Explanation["Z[i] = length of longest substring<br/>starting from i that matches prefix"]
        
        Example1["Z[3] = 3: 'ABC' matches prefix 'ABC'"]
        Example2["Z[6] = 3: 'ABC' matches prefix 'ABC'"]
    end
    
    subgraph "Pattern Matching Application"
        Concat["Concatenate: Pattern + '$' + Text"]
        Search["Find Z-values equal to pattern length"]
        Locate["Those positions indicate matches"]
    end
```

### Z-Algorithm Optimization

```mermaid
graph LR
    subgraph "Z-Box Optimization"
        ZBox["Maintain rightmost Z-box [l,r]<br/>where s[l...r] = s[0...r-l]"]
        
        Case1["Case 1: i > r<br/>Compute Z[i] from scratch"]
        Case2["Case 2: i ≤ r<br/>Use previously computed values"]
        
        ZBox --> Case1
        ZBox --> Case2
    end
    
    Complexity["Time: O(n)<br/>Each character examined at most twice"]
```

## Wildcard Pattern Matching

### Dynamic Programming Approach

```mermaid
graph TB
    subgraph "DP Table for Pattern 'a*b' and Text 'acb'"
        Table["
        |   | ε | a | c | b |
        |---|---|---|---|---|
        | ε | T | F | F | F |
        | a | F | T | F | F |
        | * | F | T | T | T |
        | b | F | F | F | T |
        "]
        
        Rules["
        Rules:
        • ε matches ε: True
        • char matches char: diagonal
        • * matches anything: OR of (left, top, diagonal)
        • ? matches single char: diagonal if match
        "]
    end
```

### State Transition Visualization

```mermaid
stateDiagram-v2
    [*] --> ε : Start
    ε --> a : Match 'a'
    a --> star : Encounter '*'
    star --> star : Match any char (stay in *)
    star --> b : Try to match 'b'
    b --> [*] : Pattern complete
    
    note right of star : Asterisk can match<br/>zero or more characters
```

## Regular Expression Matching

### NFA Construction

```mermaid
graph LR
    subgraph "NFA for Pattern 'a*b'"
        S0((0)) --> S1((1))
        S1 --> S1
        S1 --> S2((2))
        S2 --> S3(((3)))
        
        S0 -.->|ε| S1
        S1 -.->|ε| S2
    end
    
    Labels["
    0→1: match 'a'
    1→1: match 'a' (loop for *)
    1→2: ε-transition (skip *)
    2→3: match 'b'
    "]
```

### Backtracking vs DP

```mermaid
graph TB
    subgraph "Approach Comparison"
        Backtrack["Backtracking:<br/>• Recursive exploration<br/>• May revisit states<br/>• Exponential worst case"]
        
        DP["Dynamic Programming:<br/>• Memoized states<br/>• Bottom-up computation<br/>• Polynomial time"]
        
        Choice["Choose DP for:<br/>• Interview settings<br/>• Optimal complexity<br/>• Clear reasoning"]
    end
```

## Algorithm Selection Guide

```mermaid
flowchart TD
    Start([Pattern Matching Problem]) --> Q1{Single Pattern?}
    
    Q1 -->|Yes| Q2{Pattern Length?}
    Q1 -->|No| MultiplePatterns[Aho-Corasick Algorithm<br/>O(n + m + z)]
    
    Q2 -->|Short <10| BruteForce[Brute Force<br/>O(nm)]
    Q2 -->|Medium| Q3{Text Length?}
    Q2 -->|Long >1000| BoyerMoore[Boyer-Moore<br/>O(n/m) average]
    
    Q3 -->|Large| RabinKarp[Rabin-Karp<br/>O(n+m) expected]
    Q3 -->|Medium| KMP[KMP Algorithm<br/>O(n+m) guaranteed]
    
    Q4{Special Characters?}
    Q4 -->|Wildcards| Wildcards[DP Approach<br/>O(nm)]
    Q4 -->|Regex| Regex[NFA/DP<br/>O(nm)]
    Q4 -->|None| Q2
```

## Performance Summary

```mermaid
graph TB
    subgraph "Algorithm Comparison"
        A["Brute Force: O(nm) time, O(1) space"]
        B["KMP: O(n+m) time, O(m) space"]
        C["Boyer-Moore: O(n/m) avg, O(nm) worst, O(m) space"]
        D["Rabin-Karp: O(n+m) expected, O(nm) worst, O(1) space"]
        E["Z-Algorithm: O(n+m) time, O(n+m) space"]
    end
    
    subgraph "Use Cases"
        U1["Small patterns → Brute Force"]
        U2["Guaranteed performance → KMP"]
        U3["Large alphabet, long patterns → Boyer-Moore"]
        U4["Rolling hash applications → Rabin-Karp"]
        U5["Multiple pattern occurrences → Z-Algorithm"]
    end
```

## Implementation Tips

1. **Preprocessing**: Build auxiliary structures (failure function, hash) before main algorithm
2. **Edge Cases**: Empty pattern, pattern longer than text, single character patterns
3. **Overflow**: Use modular arithmetic for rolling hash to prevent overflow
4. **Multiple Matches**: Decide whether to find first, all, or count occurrences
5. **Case Sensitivity**: Handle uppercase/lowercase requirements consistently

## Next: [Dynamic Programming on Strings →](dynamic-programming.md)
# Basic String Operations - Visual Guide

This guide covers fundamental string operations with step-by-step visualizations and complexity analysis.

## String Reversal Algorithms

### Two-Pointer Approach (In-Place)

```mermaid
graph TB
    subgraph "Step-by-Step Reversal of 'hello'"
        S0["Initial: h e l l o<br/>Left: 0, Right: 4"]
        S1["Swap: o e l l h<br/>Left: 1, Right: 3"]
        S2["Swap: o l l e h<br/>Left: 2, Right: 2"]
        S3["Final: o l l e h<br/>Complete!"]
        
        S0 --> S1 --> S2 --> S3
    end
    
    subgraph "Algorithm Steps"
        A1[Initialize left=0, right=n-1]
        A2[While left < right]
        A3[Swap chars at left and right]
        A4[Increment left, decrement right]
        
        A1 --> A2 --> A3 --> A4 --> A2
    end
```

**Complexity:** Time O(n), Space O(1)

### Recursive Approach

```mermaid
flowchart TD
    F1["reverse('hello')"] --> F2["'o' + reverse('ell') + 'h'"]
    F2 --> F3["'o' + ('l' + reverse('l') + 'l') + 'h'"]
    F3 --> F4["'o' + ('l' + 'l' + 'l') + 'h'"]
    F4 --> F5["Result: 'olleh'"]
    
    Base["Base case: single char or empty → return as is"]
```

**Complexity:** Time O(n), Space O(n) due to call stack

## Character Frequency Analysis

### HashMap-Based Counting

```mermaid
graph TB
    subgraph "Processing 'hello world'"
        Input["h e l l o   w o r l d"]
        
        subgraph "HashMap Updates"
            H1["h: 1"]
            H2["e: 1, h: 1"]
            H3["l: 1, e: 1, h: 1"]
            H4["l: 2, e: 1, h: 1"]
            H5["o: 1, l: 2, e: 1, h: 1"]
            H6["space: 1, o: 1, l: 2, e: 1, h: 1"]
            H7["Final: {h:1, e:1, l:3, o:2, space:1, w:1, r:1, d:1}"]
        end
    end
    
    Algorithm["For each character:<br/>1. Check if in map<br/>2. Increment count<br/>3. Add if new"]
```

### Array-Based Counting (ASCII)

```mermaid
graph LR
    subgraph "ASCII Array Approach"
        A["Array[128] initialized to 0"]
        B["For char c: array[ord(c)]++"]
        C["Space efficient for ASCII"]
    end
    
    subgraph "Example: count('abc')"
        E1["array[97] = 1  // 'a'"]
        E2["array[98] = 1  // 'b'"]
        E3["array[99] = 1  // 'c'"]
    end
```

**Complexity:** Time O(n), Space O(1) for ASCII, O(k) for Unicode

## Subsequence Detection

### Two-Pointer Technique

```mermaid
sequenceDiagram
    participant S as Source: "abcde"
    participant T as Target: "ace"
    participant P1 as Pointer1
    participant P2 as Pointer2
    
    Note over S,T: Initial state
    P1->>S: Position 0 ('a')
    P2->>T: Position 0 ('a')
    
    Note over S,T: Match found, advance both
    P1->>S: Position 1 ('b')
    P2->>T: Position 1 ('c')
    
    Note over S,T: No match, advance source only
    P1->>S: Position 2 ('c')
    P2->>T: Position 1 ('c')
    
    Note over S,T: Match found, advance both
    P1->>S: Position 3 ('d')
    P2->>T: Position 2 ('e')
    
    Note over S,T: No match, advance source only
    P1->>S: Position 4 ('e')
    P2->>T: Position 2 ('e')
    
    Note over S,T: Match found - subsequence valid!
```

## String Rotation

### Left Rotation by K Positions

```mermaid
graph TB
    subgraph "Rotate 'abcdef' left by 2"
        Original["a b c d e f"]
        Step1["Split at position 2:<br/>Part1: 'ab'<br/>Part2: 'cdef'"]
        Result["c d e f a b"]
        
        Original --> Step1 --> Result
    end
    
    subgraph "Efficient Approach: Triple Reverse"
        A["Original: abcdef"]
        B["Reverse all: fedcba"]
        C["Reverse first (n-k): cdefba"]
        D["Reverse last k: cdefab"]
        
        A --> B --> C --> D
    end
```

**Algorithm Steps:**
1. Reverse entire string
2. Reverse first (n-k) characters  
3. Reverse last k characters

**Complexity:** Time O(n), Space O(1)

## Duplicate Removal

### Preserve Order Approach

```mermaid
flowchart TD
    Input["Input: 'programming'"] --> Process
    
    subgraph Process["Processing with HashSet"]
        S1["Char 'p': seen={p}, result='p'"]
        S2["Char 'r': seen={p,r}, result='pr'"]
        S3["Char 'o': seen={p,r,o}, result='pro'"]
        S4["Char 'g': seen={p,r,o,g}, result='prog'"]
        S5["Char 'r': already seen, skip"]
        S6["Char 'a': seen={p,r,o,g,a}, result='proga'"]
        S7["Continue until 'm': result='progamin'"]
        
        S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
    end
    
    Process --> Output["Output: 'progamin'"]
```

### Two-Pointer In-Place (Sorted String)

```mermaid
graph LR
    subgraph "Remove duplicates from 'aabbcc'"
        State1["a a b b c c<br/>↑write ↑read"]
        State2["a _ b b c c<br/>  ↑write   ↑read"]
        State3["a b _ c c c<br/>    ↑write   ↑read"]
        State4["a b c _ _ _<br/>      ↑write"]
        
        State1 --> State2 --> State3 --> State4
    end
    
    Rule["Rule: Only write if current != previous"]
```

## Most Frequent Character

### Single Pass with Tracking

```mermaid
graph TB
    subgraph "Find most frequent in 'hello'"
        Process["
        h: count=1, max_char='h', max_count=1
        e: count=1, max unchanged
        l: count=1, max unchanged
        l: count=2, max_char='l', max_count=2
        o: count=1, max unchanged
        Result: 'l' with count 2
        "]
    end
    
    subgraph "Data Structure"
        FreqMap["HashMap: char → count"]
        MaxTracker["Variables: max_char, max_count"]
        
        FreqMap --> MaxTracker
    end
```

## First Unique Character

### Two-Pass Approach

```mermaid
flowchart LR
    subgraph "Input: 'leetcode'"
        Pass1["Pass 1: Count frequencies<br/>{l:1, e:3, t:1, c:1, o:1, d:1}"]
        Pass2["Pass 2: Find first with count=1<br/>Index 0: 'l' has count 1 ✓"]
        
        Pass1 --> Pass2
    end
    
    Result["Return index: 0"]
```

### Single-Pass Approach

```mermaid
graph TB
    subgraph "Optimized Single Pass"
        Data["HashMap: char → first_index"]
        Logic["
        If char seen before:
          Mark as duplicate (index = -1)
        Else:
          Store current index
        
        Return minimum valid index
        "]
        
        Data --> Logic
    end
```

## Performance Comparison

```mermaid
graph TB
    subgraph "Algorithm Complexity Comparison"
        A["String Reversal"]
        A1["Two-pointer: O(n) time, O(1) space"]
        A2["Recursive: O(n) time, O(n) space"]
        A3["New string: O(n) time, O(n) space"]
        
        B["Frequency Count"]
        B1["HashMap: O(n) time, O(k) space"]
        B2["Array (ASCII): O(n) time, O(1) space"]
        B3["Sorting: O(n log n) time, O(1) space"]
        
        A --> A1
        A --> A2  
        A --> A3
        B --> B1
        B --> B2
        B --> B3
    end
```

## Practice Problems Mapping

```mermaid
mindmap
  root((Basic String Operations))
    Character Analysis
      Frequency counting
      Most/least frequent
      First unique character
      Character replacement
    String Manipulation
      Reversal algorithms
      Rotation detection
      Case conversion
      Remove duplicates
    Subsequence Problems
      Is subsequence
      Longest common subsequence
      Delete characters
      String matching
    Comparison Operations
      String equality
      Lexicographic order
      Anagram detection
      Pattern validation
```

## Key Insights

1. **In-place vs Extra Space**: Consider memory constraints
2. **ASCII vs Unicode**: Choose appropriate data structures
3. **Single vs Multiple Pass**: Balance between time and space
4. **Edge Cases**: Empty strings, single characters, all same characters
5. **Optimization**: Use bit manipulation for character sets when possible

## Next: [Pattern Matching Algorithms →](pattern-matching.md)
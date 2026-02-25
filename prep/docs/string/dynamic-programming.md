# Dynamic Programming on Strings - Visual Guide

This guide covers essential string DP problems with detailed visualizations and state transition analysis.

## DP on Strings Problem Categories

```mermaid
mindmap
  root((String DP Problems))
    Edit Distance
      Levenshtein Distance
      Edit operations count
      Transformation path
      Space optimization
    Longest Common
      LCS - Subsequence
      LCString - Substring  
      Multiple sequences
      Print actual sequence
    Palindromes
      Longest palindromic subsequence
      Palindrome partitioning
      Minimum insertions
      Count palindromes
    String Matching
      Wild card matching
      Regular expressions
      Pattern with * and ?
      Case variations
    Word Problems
      Word break
      Word break II
      Sentence construction
      Dictionary validation
    Advanced Applications
      Interleaving strings
      Distinct subsequences
      Scramble string
      Decode ways
```

## Edit Distance (Levenshtein Distance)

### State Definition and Recurrence

```mermaid
graph TB
    subgraph "State Definition"
        State["dp[i][j] = minimum operations to transform<br/>first i characters of string1<br/>to first j characters of string2"]
    end
    
    subgraph "Operations"
        Insert["Insert: dp[i][j-1] + 1"]
        Delete["Delete: dp[i-1][j] + 1"] 
        Replace["Replace: dp[i-1][j-1] + cost"]
        Cost["cost = 0 if chars match, 1 if different"]
    end
    
    subgraph "Recurrence"
        Formula["dp[i][j] = min(<br/>dp[i-1][j] + 1,    // delete<br/>dp[i][j-1] + 1,    // insert<br/>dp[i-1][j-1] + cost // replace<br/>)"]
    end
```

### Step-by-Step Example: "horse" → "ros"

```mermaid
graph TB
    subgraph "DP Table Construction"
        Table["
        |   | ε | r | o | s |
        |---|---|---|---|---|
        | ε | 0 | 1 | 2 | 3 |
        | h | 1 | 1 | 2 | 3 |
        | o | 2 | 2 | 1 | 2 |
        | r | 3 | 2 | 2 | 2 |
        | s | 4 | 3 | 3 | 2 |
        | e | 5 | 4 | 4 | 3 |
        "]
        
        Operations["
        Final answer: 3 operations
        1. Replace h→r: 'rorse'
        2. Delete o: 'rrse' 
        3. Replace r→o: 'rose'
        Actually optimal: Delete h, Delete o, Delete r → 'rse' → 'ros'
        "]
    end
```

### Space Optimization

```mermaid
graph LR
    subgraph "2D Array Approach"
        A["Space: O(m×n)<br/>Keep entire table"]
    end
    
    subgraph "1D Array Optimization"  
        B["Space: O(min(m,n))<br/>Only keep current and previous row"]
        
        Update["For each cell, only need:<br/>• Current row up to j-1<br/>• Previous row at j and j-1"]
    end
    
    A --> B
```

## Longest Common Subsequence (LCS)

### LCS Recurrence Relation

```mermaid
graph TB
    subgraph "LCS State Definition"
        LCSState["dp[i][j] = length of LCS of<br/>first i chars of string1 and<br/>first j chars of string2"]
    end
    
    subgraph "Recurrence Logic"
        Match["If s1[i-1] == s2[j-1]:<br/>dp[i][j] = dp[i-1][j-1] + 1"]
        NoMatch["Else:<br/>dp[i][j] = max(dp[i-1][j], dp[i][j-1])"]
    end
```

### LCS Example: "ABCDGH" and "AEDFHR"

```mermaid
graph TB
    subgraph "LCS DP Table"
        LCSTable["
        |   | ε | A | E | D | F | H | R |
        |---|---|---|---|---|---|---|---|
        | ε | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
        | A | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
        | B | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
        | C | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
        | D | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
        | G | 0 | 1 | 1 | 2 | 2 | 2 | 2 |
        | H | 0 | 1 | 1 | 2 | 2 | 3 | 3 |
        "]
        
        Result["LCS length: 3<br/>Actual LCS: 'ADH'"]
    end
```

### Reconstructing the LCS

```mermaid
flowchart TD
    Start["Start at dp[m][n]"] --> Check{s1[i-1] == s2[j-1]?}
    
    Check -->|Yes| AddChar["Add character to LCS<br/>Move to dp[i-1][j-1]"]
    Check -->|No| Compare{dp[i-1][j] > dp[i][j-1]?}
    
    Compare -->|Yes| MoveUp["Move to dp[i-1][j]"]
    Compare -->|No| MoveLeft["Move to dp[i][j-1]"]
    
    AddChar --> End{Reached dp[0][0]?}
    MoveUp --> End
    MoveLeft --> End
    
    End -->|No| Check
    End -->|Yes| Reverse["Reverse LCS string"]
```

## Longest Palindromic Subsequence

### State Definition and Transitions

```mermaid
graph TB
    subgraph "Palindromic Subsequence DP"
        PalState["dp[i][j] = length of longest palindromic<br/>subsequence in substring s[i...j]"]
        
        BaseCase["Base cases:<br/>dp[i][i] = 1 (single char)<br/>dp[i][i+1] = 2 if s[i]==s[i+1], else 1"]
        
        Transition["If s[i] == s[j]:<br/>dp[i][j] = dp[i+1][j-1] + 2<br/>Else:<br/>dp[i][j] = max(dp[i+1][j], dp[i][j-1])"]
    end
```

### Example: "bbbab"

```mermaid
graph TB
    subgraph "LPS Table for 'bbbab'"
        LPSTable["
        |   | b | b | b | a | b |
        |---|---|---|---|---|---|
        | b | 1 | 2 | 3 | 3 | 4 |
        | b |   | 1 | 2 | 2 | 3 |
        | b |   |   | 1 | 1 | 3 |
        | a |   |   |   | 1 | 1 |
        | b |   |   |   |   | 1 |
        "]
        
        Explanation["Fill diagonally from bottom-right<br/>LPS length: 4<br/>Actual LPS: 'bbbb' or 'babb'"]
    end
```

## Word Break Problem

### DP Approach for Word Break

```mermaid
graph TB
    subgraph "Word Break State"
        WBState["dp[i] = true if substring s[0...i-1]<br/>can be segmented using dictionary words"]
    end
    
    subgraph "Transition Logic"
        WBLogic["For each position i:<br/>For each position j < i:<br/>  if dp[j] && dict.contains(s[j...i-1]):<br/>    dp[i] = true<br/>    break"]
    end
```

### Example: "leetcode" with dictionary ["leet", "code"]

```mermaid
sequenceDiagram
    participant S as String: "leetcode"
    participant D as Dictionary: ["leet", "code"]
    participant DP as DP Array
    
    Note over S,DP: Initialize dp[0] = true
    
    S->>DP: Check "l": not in dict, dp[1] = false
    S->>DP: Check "le": not in dict, dp[2] = false  
    S->>DP: Check "lee": not in dict, dp[3] = false
    S->>DP: Check "leet": in dict!, dp[4] = true
    
    S->>DP: Check "leetc": "c" not in dict, dp[5] = false
    S->>DP: Check "leetco": "co" not in dict, dp[6] = false
    S->>DP: Check "leetcod": "cod" not in dict, dp[7] = false
    S->>DP: Check "leetcode": "code" in dict and dp[4]=true!, dp[8] = true
    
    Note over S,DP: Result: true (can be segmented)
```

## Wildcard Pattern Matching

### State Transitions for Wildcards

```mermaid
graph TB
    subgraph "Wildcard DP States"
        WildState["dp[i][j] = true if first i characters of text<br/>match first j characters of pattern"]
        
        Cases["
        Case 1: pattern[j-1] == text[i-1] or pattern[j-1] == '?'
               → dp[i][j] = dp[i-1][j-1]
        
        Case 2: pattern[j-1] == '*'
               → dp[i][j] = dp[i-1][j] OR dp[i][j-1] OR dp[i-1][j-1]
               (match one more char, skip *, or skip both)
        
        Case 3: No match
               → dp[i][j] = false
        "]
    end
```

### Example: Text "adceb", Pattern "a*b"

```mermaid
graph TB
    subgraph "Wildcard Matching Table"
        WTable["
        |     | ε | a | * | b |
        |-----|---|---|---|---|
        | ε   | T | F | T | F |
        | a   | F | T | T | F |
        | d   | F | F | T | F |
        | c   | F | F | T | F |
        | e   | F | F | T | F |
        | b   | F | F | T | T |
        "]
        
        Trace["* can match zero or more characters<br/>Final result: True<br/>Path: a matches 'a', * matches 'dce', b matches 'b'"]
    end
```

## Advanced String DP Problems

### Interleaving Strings

```mermaid
graph TB
    subgraph "Interleaving DP"
        IntState["dp[i][j] = true if first i chars of s1<br/>and first j chars of s2 can form<br/>first i+j chars of s3"]
        
        IntTransition["
        If s1[i-1] == s3[i+j-1] and dp[i-1][j]:
          dp[i][j] = true
        If s2[j-1] == s3[i+j-1] and dp[i][j-1]:
          dp[i][j] = true
        "]
    end
```

### Distinct Subsequences

```mermaid
graph TB
    subgraph "Distinct Subsequences DP"
        DistState["dp[i][j] = number of ways to form<br/>first j chars of target using<br/>first i chars of source"]
        
        DistLogic["
        If source[i-1] == target[j-1]:
          dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
          (use this char + skip this char)
        Else:
          dp[i][j] = dp[i-1][j]
          (skip this char)
        "]
    end
```

## Complexity Analysis Summary

```mermaid
graph TB
    subgraph "DP String Problems Complexity"
        EditDist["Edit Distance:<br/>Time: O(mn), Space: O(mn)→O(min(m,n))"]
        LCS["LCS:<br/>Time: O(mn), Space: O(mn)→O(min(m,n))"]
        LPS["Longest Palindromic Subsequence:<br/>Time: O(n²), Space: O(n²)→O(n)"]
        WordBreak["Word Break:<br/>Time: O(n²), Space: O(n)"]
        Wildcard["Wildcard Matching:<br/>Time: O(mn), Space: O(mn)→O(n)"]
        Interleave["Interleaving:<br/>Time: O(mn), Space: O(mn)→O(min(m,n))"]
    end
```

## Problem-Solving Strategy

```mermaid
flowchart TD
    Problem[String DP Problem] --> Identify{Identify Pattern}
    
    Identify -->|Two Strings| TwoString[Edit Distance, LCS, Interleaving]
    Identify -->|Single String| SingleString[LPS, Palindrome Partitioning]
    Identify -->|Pattern Matching| Pattern[Wildcard, Regex]
    Identify -->|Dictionary| Dict[Word Break, Sentence]
    
    TwoString --> Define2D[Define dp[i][j] for positions in both strings]
    SingleString --> Define1D[Define dp[i][j] for substring range]
    Pattern --> DefineMatch[Define dp[i][j] for text vs pattern]
    Dict --> DefineBreak[Define dp[i] for prefix breakability]
    
    Define2D --> BaseCase[Set base cases]
    Define1D --> BaseCase
    DefineMatch --> BaseCase
    DefineBreak --> BaseCase
    
    BaseCase --> Transition[Define state transitions]
    Transition --> Optimize[Consider space optimization]
```

## Key Insights

1. **State Design**: Clearly define what each DP state represents
2. **Base Cases**: Handle empty strings and single characters correctly
3. **Transitions**: Consider all possible operations (match, skip, transform)
4. **Space Optimization**: Often can reduce from 2D to 1D array
5. **Reconstruction**: If path/sequence needed, store parent pointers or trace back
6. **Edge Cases**: Empty strings, identical strings, completely different strings

## Next: [Advanced String Problems →](advanced-problems.md)
from abk_aapl.solution import solution

k = 3
a = [1, 6, 8, 2, 4, 9, 12]
result = solution(k, a)
print(f"Result: {result}")
print("Expected: 3")

# Verify pairs manually
pairs = []
for i in range(len(a)):
    for j in range(len(a)):
        if i != j and a[j] - a[i] == k:
            pairs.append((a[i], a[j]))

print(f"Pairs found: {pairs}")

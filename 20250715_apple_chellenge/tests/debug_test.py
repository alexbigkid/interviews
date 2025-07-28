from abk_aapl.simple_solution import solution

# Debug the failing test
a = [1, 2, 1001, 1002]
k = 1000
result = solution(k, a)
print(f"Result: {result}")

# Check what pairs exist
pairs = []
for i in range(len(a)):
    for j in range(len(a)):
        if i != j and a[j] - a[i] == k:
            pairs.append((a[i], a[j]))

print(f"Pairs found: {pairs}")
print(f"Expected: 1, Got: {result}")

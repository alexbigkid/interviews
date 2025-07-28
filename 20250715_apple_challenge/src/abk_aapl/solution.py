def solution(k: int, a: list[int]) -> int:
    MOD = 10**9 + 7

    if not a:
        return 0

    count = {}

    for num in a:
        count[num] = count.get(num, 0) + 1

    pairs = 0
    for num in count:
        target = num + k
        if target in count:
            pairs = (pairs + count[num] * count[target]) % MOD

    return pairs

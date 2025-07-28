def solution(k: int, a: list[int]) -> int:
    if not a:
        return 0

    count = {}
    for num in a:
        count[num] = count.get(num, 0) + 1

    pairs = 0
    for num in count:
        if num + k in count:
            pairs += count[num] * count[num + k]

    return pairs % (10**9 + 7)

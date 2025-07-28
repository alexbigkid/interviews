import time
from abk_aapl.simple_solution import solution


def test_performance():
    """Test performance with large inputs"""
    print("Testing performance with large inputs...")

    # Test 1: Maximum array size (10^5 elements)
    print("\nTest 1: Maximum array size")
    large_array = list(range(1, 100001))  # 100,000 elements
    start_time = time.time()
    result = solution(1, large_array)
    end_time = time.time()
    print(f"Array size: {len(large_array)}")
    print(f"Result: {result}")
    print(f"Time: {end_time - start_time:.4f} seconds")

    # Test 2: Many duplicates
    print("\nTest 2: Many duplicates")
    duplicate_array = [1] * 50000 + [2] * 50000
    start_time = time.time()
    result = solution(1, duplicate_array)
    end_time = time.time()
    print(f"Array size: {len(duplicate_array)}")
    print(f"Result: {result}")
    print(f"Time: {end_time - start_time:.4f} seconds")

    # Test 3: Large numbers (within constraint)
    print("\nTest 3: Large numbers")
    large_nums = [999, 1000] * 50000
    start_time = time.time()
    result = solution(1, large_nums)
    end_time = time.time()
    print(f"Array size: {len(large_nums)}")
    print(f"Result: {result}")
    print(f"Time: {end_time - start_time:.4f} seconds")

    # Test 4: Maximum k value
    print("\nTest 4: Maximum k value")
    max_k_array = [1, 1001] * 1000
    start_time = time.time()
    result = solution(1000, max_k_array)
    end_time = time.time()
    print(f"Array size: {len(max_k_array)}")
    print("k value: 1000")
    print(f"Result: {result}")
    print(f"Time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    test_performance()

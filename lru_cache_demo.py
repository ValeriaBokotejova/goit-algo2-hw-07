"""
Demonstrate LRU cache vs no-cache for range-sum and update operations.
"""

import time
import random
from collections import OrderedDict
from colorama import Fore, Style

# Configuration
N = 100_000     # array size
Q = 50_000      # number of queries
CACHE_CAP = 1000  # capacity of LRU cache

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.capacity:
            self.od.popitem(last=False)

    def invalidate_index(self, idx):
        keys_to_remove = [k for k in self.od.keys() if k[0] <= idx <= k[1]]
        for k in keys_to_remove:
            del self.od[k]

def range_sum_no_cache(array, left, right):
    return sum(array[left:right+1])

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, cache: LRUCache, left, right):
    key = (left, right)
    v = cache.get(key)
    if v != -1:
        return v
    v = sum(array[left:right+1])
    cache.put(key, v)
    return v

def update_with_cache(array, cache: LRUCache, index, value):
    array[index] = value
    cache.invalidate_index(index)

def main():
    # Generate data
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    # No-cache run
    arr1 = list(array)
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            _, l, r = q
            _ = range_sum_no_cache(arr1, l, r)
        else:
            _, idx, val = q
            update_no_cache(arr1, idx, val)
    t_no_cache = time.time() - start

    # With-cache run
    arr2 = list(array)
    cache = LRUCache(CACHE_CAP)
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            _, l, r = q
            _ = range_sum_with_cache(arr2, cache, l, r)
        else:
            _, idx, val = q
            update_with_cache(arr2, cache, idx, val)
    t_with_cache = time.time() - start

    # Output results
    speedup = t_no_cache / t_with_cache if t_with_cache > 0 else float('inf')
    print(f"{Fore.MAGENTA}Without cache:{Style.RESET_ALL} {t_no_cache:.2f} s")
    print(f"{Fore.GREEN}With LRU cache:{Style.RESET_ALL} {t_with_cache:.2f} s  (speedup ×{speedup:.2f})")

if __name__ == '__main__':
    main()

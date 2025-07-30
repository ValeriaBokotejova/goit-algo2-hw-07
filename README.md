# Cache Management Algorithms Homework 🗄️⚡
_repo: goit-algo2-hw-07_

Two exercises showcasing caching strategies and their impact on performance.

---

## ⚙️ Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 1️⃣ Task 1: LRU Cache for Range‐Sum Queries

**File:**

`lru_cache_demo.py`

**Implement:**

- `range_sum_no_cache(array, L, R)`
- `update_no_cache(array, i, v)`
- `range_sum_with_cache(array, cache, L, R) (LRU capacity 1000)`
- `update_with_cache(array, cache, i, v)`

**Run:**

```bash
python lru_cache_demo.py
```
Prints timings "Without cache: xx.xx s" vs "With LRU cache: yy.yy s (speedup ×z.z)".

---

## 2️⃣ Task 2: Fibonacci via LRU Cache vs Splay Tree

**File:** 

`fib_compare.py`

**Implement:**

- `fibonacci_lru(n)` with `@functools.lru_cache`
- `fibonacci_splay(n, tree)` with a custom Splay Tree memo
- Benchmark:
    Measures average time for n = 0, 50, 100…950, prints a Markdown table and plots a comparison graph.

**Run:**

```bash
python fib_compare.py
```

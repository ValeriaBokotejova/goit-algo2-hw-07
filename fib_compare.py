"""
Compare Fibonacci computation using @lru_cache vs. Splay Tree memoization.
"""

import sys
import timeit
import functools
import matplotlib.pyplot as plt
from tabulate import tabulate
from colorama import Fore, Style

sys.setrecursionlimit(2000)

@functools.lru_cache(maxsize=None)
def fibonacci_lru(n: int) -> int:
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate(self, x):
        p = x.parent
        if p is None:
            return
        g = p.parent
        if x is p.left:
            # right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            # left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if p is g.left:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                # zig
                self._rotate(x)
            elif (x is p.left) == (p is g.left):
                # zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # zig-zag
                self._rotate(x)
                self._rotate(x)

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        node = self.root
        while True:
            if key == node.key:
                node.value = value
                self._splay(node)
                return
            elif key < node.key:
                if node.left is None:
                    new = SplayNode(key, value)
                    node.left = new
                    new.parent = node
                    self._splay(new)
                    return
                node = node.left
            else:
                if node.right is None:
                    new = SplayNode(key, value)
                    node.right = new
                    new.parent = node
                    self._splay(new)
                    return
                node = node.right

    def search(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                self._splay(node)
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        # splay last accessed
        if last:
            self._splay(last)
        return None

def fibonacci_splay(n: int, tree: SplayTree) -> int:
    # check cache
    val = tree.search(n)
    if val is not None:
        return val
    # compute
    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

def measure_times(ns, repeats=3):
    lru_times = []
    splay_times = []
    for n in ns:
        # LRU
        fibonacci_lru.cache_clear()
        t_lru = sum(timeit.repeat(lambda: fibonacci_lru(n), repeat=repeats, number=1)) / repeats
        # Splay
        t_spl = sum(timeit.repeat(lambda: fibonacci_splay(n, SplayTree()),
                                  repeat=repeats, number=1)) / repeats
        lru_times.append(t_lru)
        splay_times.append(t_spl)
    return lru_times, splay_times

def main():
    ns = list(range(0, 951, 50))
    repeats = 3

    lru_times, splay_times = measure_times(ns, repeats)

    # Print table
    table = []
    for n, t_l, t_s in zip(ns, lru_times, splay_times):
        table.append([n, f"{t_l:.8f}", f"{t_s:.8f}"])
    print("\nBenchmark results:\n")
    headers = [Fore.MAGENTA + "n" + Style.RESET_ALL,
               Fore.MAGENTA + "LRU Cache Time (s)" + Style.RESET_ALL,
               Fore.MAGENTA + "Splay Tree Time (s)" + Style.RESET_ALL]
    print(
        tabulate(
            table, 
            headers=headers, 
            tablefmt="github", 
            numalign="center", 
            stralign="center"), 
        "\n"
    )

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(ns, lru_times, marker='o', label='LRU Cache')
    plt.plot(ns, splay_times, marker='x', label='Splay Tree')
    plt.title("Execution Time: LRU Cache vs Splay Tree")
    plt.xlabel("Fibonacci n")
    plt.ylabel("Average time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

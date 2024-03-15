import math
import re
import time

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    res = aocu.reduce_input(res)  # dimensionality reduction
    res = [r[1:] for r in res]
    res = [(x, y) for x, y in zip(res[0], res[1])]
    # ⬆ a lot of ugly boiler plate code to get the (time, distance) pair list ⬇
    return res


def get_roots(a, b, c):
    d = b**2 - 4 * a * c
    return None if d < 0 else ((-b - d**0.5) / (2 * a), (-b + d**0.5) / (2 * a))


def get_record_count(t, d):
    roots = get_roots(1, -t, d)
    if roots is not None:
        t1, t2 = roots
        t1 = math.floor(t1) + 1
        t2 = math.ceil(t2) - 1
        return max(t2 - t1 + 1, 0)
    return 0


def solve_1(values):
    n_sols = 1
    for t, d in values:
        n_sols *= get_record_count(t, d) or 1
    return n_sols


def solve_2(values):
    T, D = "", ""
    for t, d in values:
        T += f"{t}"
        D += f"{d}"
    T, D = int(T), int(D)
    return get_record_count(T, D)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

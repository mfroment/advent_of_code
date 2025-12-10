import re
import time

import aoc.utils as aocu

import functools


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [[aocu.s2i(v) for v in re.split(r"-", t)] for t in re.split(r",", line)]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    invalids = set()
    for start, end in values:
        for v in range(start, end + 1):
            length = len(str(v))
            if length % 2 != 0:
                continue
            block = 10 ** (length // 2)
            if v // block == v % block:
                invalids.add(v)
    return sum(invalids)


@functools.cache
def divisors(n):
    assert n > 0
    res = [1]
    for i in range(2, n):
        if n % i == 0:
            res.append(i)
    return res


def solve_2(values):
    invalids = set()
    for start, end in values:
        for v in range(start, end + 1):
            vs = str(v)
            if len(vs) == 1:  # nice trap... not...
                continue
            length = len(vs)
            divs = divisors(length)
            for d in divs:
                if vs == (vs[:d] * (length // d)):
                    invalids.add(v)
                    break
    return sum(invalids)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

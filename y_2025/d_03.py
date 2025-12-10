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
            tokens = [aocu.s2i(i) for t in tokens for i in t]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def jolt(v, size):
    assert size >= 0
    assert len(v) >= size

    if size == 0:
        return 0
    # search max in a copy-slice, then look it up again, then recurse on another copy-slice, while not ideal, does not impact complexity and works at the scale of the problem
    lead = max(v[: -size + 1] if size > 1 else v)
    i = v.index(lead)
    res = lead * (10 ** (size - 1)) + jolt(v[i + 1 :], size - 1)
    return res


def solve_1(values):
    return sum(jolt(v, 2) for v in values)


def solve_2(values):
    return sum(jolt(v, 12) for v in values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

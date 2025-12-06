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
    id_ranges, ids = aocu.reduce_input(res)  # dimensionality reduction
    ids = [i[0] for i in ids]
    return (id_ranges, ids)


def solve_1(values):
    id_ranges, ids = values
    return sum((1 if any(r[0] <= i <= r[1] for r in id_ranges) else 0) for i in ids)


def merge_ranges(ranges):
    res = []
    for r in sorted(ranges):
        if res and res[-1][1] >= r[0]-1:
            res[-1][1] = max(res[-1][1], r[1])
        else:
            res.append(r)
    return res


def solve_2(values):
    id_ranges, _ = values
    return sum( r[1]-r[0]+1 for r in merge_ranges(id_ranges))


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

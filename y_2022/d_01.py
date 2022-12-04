import time
import re
import aoc_utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [aocu.s2i(line)]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


def sorted_sums(values):
    return list(reversed(sorted([sum(v) for v in values])))


def solve_1(values):
    return sorted_sums(values)[0]


def solve_2(values):
    return sum(sorted_sums(values)[0:3])


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

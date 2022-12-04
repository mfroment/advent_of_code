import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


def is_included(a, b, c, d):
    return (a <= c and b >= d) or (c <= a and d >= b)


def is_overlapping(a, b, c, d):
    return not (b < c or a > d)


def count_if(values, condition):
    return sum(1 if condition(v) else 0 for v in values)


def solve_1(values):
    return count_if(values, lambda v: is_included(*v))


def solve_2(values):
    return count_if(values, lambda v: is_overlapping(*v))


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

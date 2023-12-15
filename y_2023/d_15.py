import time
import re
import aoc.utils as aocu
from functools import cache


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",", line, maxsplit=0)
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


@cache
def compute_hash(s, h=0):
    return h if len(s) == 0 else compute_hash(s[1:], (h + ord(s[0])) * 17 % 256)


def solve_1(values):
    return sum(compute_hash(s) for s in values)


def solve_2(values):
    lenses = dict()
    boxes = [ list() for _ in range(256) ]
    for s in values:
        if s.endswith("-"):
            s = s[:-1]
            h = compute_hash(s)
            box = boxes[h]
            if s in box:
                box.remove(s)
        else:
            s, n = s.split("=")
            h = compute_hash(s)
            n = int(n)
            box = boxes[h]
            if not s in box:
                box.append(s)
            lenses[s] = n
    p = 0
    for i_b, box in enumerate(boxes):
        for i_s, s in enumerate(box):
            p += lenses[s] * (i_b + 1) * (i_s + 1)
    return p


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

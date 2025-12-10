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
            # tokens = re.search(r"^(.+)-(.+)-(.+)-(.+)$", line).groups()
            tokens = [aocu.s2i(("+" if t[0] == "R" else "-") + t[1:]) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    count = 0
    pos = 50
    for v in values:
        pos = (pos + v) % 100
        if pos == 0:
            count += 1
    return count


def solve_2(values):
    count = 0
    pos = 50
    for v in values:
        if v < 0 and pos != 0:
            pos = pos - 100
        new_pos = pos + v
        count += (abs(new_pos) // 100) - (abs(pos) // 100)
        pos = new_pos % 100
    return count


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

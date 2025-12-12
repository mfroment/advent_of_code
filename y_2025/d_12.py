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
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    raw = aocu.reduce_input(res)  # dimensionality reduction
    presents = []
    for rp in raw[:-1]:
        presents.append(p[0] for p in rp[1:])
    regions = []
    for rp in raw[-1]:
        dx, dy, _ = re.split(r"x|:", rp[0], maxsplit=0)
        quantities = tuple(rp[1:])
        regions.append([(int(dx), int(dy)), quantities])
    return presents, regions


def present_area(present):
    return sum(1 if t == "#" else 0 for r in present for t in r)


def solve_1_upper_bound(values):
    # compute regions whose area is larger or equal than the total present area. It's an upper bound to the solution
    presents, regions = values
    present_areas = [present_area(p) for p in presents]

    possibles = 0
    for (dx, dy), present_counts in regions:
        cover = sum(a * c for a, c in zip(present_areas, present_counts))
        if cover <= dx * dy:
            possibles += 1
    return possibles


def solve_1(values):
    # no idea how to solve this in the general case
    # ... but since this problem is a troll where the upper bound actually works, it does not matter...
    return solve_1_upper_bound(values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

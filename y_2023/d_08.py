import time
import re
import aoc.utils as aocu

import math


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = aocu.reduce_input(sections)  # dimensionality reduction
    instructions = res[0][0]
    nodes = {k: (l, r) for line in res[1] for k, l, r in re.findall(r"(\w+) = \((\w+), (\w+)\)", line)}
    return instructions, nodes


def get_path_length(instructions, nodes, pos, end_condition):
    c = 0
    while not end_condition(pos):
        pos = nodes[pos][0 if instructions[c % len(instructions)] == "L" else 1]
        c += 1
    return c


def solve_1(values):
    instructions, nodes = values
    return get_path_length(instructions, nodes, "AAA", lambda pos: pos == "ZZZ")


def solve_2(values):
    instructions, nodes = values
    path_lens = [
        get_path_length(instructions, nodes, pos, lambda pos: pos.endswith("Z")) for pos in nodes if pos.endswith("A")
    ]
    return math.lcm(*path_lens)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

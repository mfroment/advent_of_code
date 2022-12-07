import time
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    return aocu.reduce_input(sections)


def solve(values, length):
    i = length
    while len(set(values[i - length:i])) != length:
        i += 1
    return i


def solve_1(values):
    return solve(values, 4)


def solve_2(values):
    return solve(values, 14)


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

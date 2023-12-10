import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",| -> |\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            tokens = [(tokens[i], tokens[i + 1]) for i in range(0, len(tokens), 2)]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def make_grid(values):
    grid = set()
    for row in values:
        grid.add(row[0])
        for i in range(1, len(row)):
            (a, b), (c, d) = row[i - 1], row[i]
            assert (a == c or b == d)
            if a == c:
                if b > d:
                    b, d = d, b
                for x in range(b, d + 1):
                    grid.add((a, x))
            else:
                if a > c:
                    a, c = c, a
                for x in range(a, c + 1):
                    grid.add((x, b))
    return grid


def solve(values):
    grid = make_grid(values)
    void = max(y for (x, y) in grid)
    for x in range(0, 1000):
        grid.add((x, void + 2))  # brute forcing here
    keep_flowing = True
    grain_count = 0
    grain_void_count = None
    while keep_flowing:
        grain_count += 1
        a, b = (500, 0)
        keep_falling = True
        while keep_falling:
            if (a, b + 1) not in grid:
                (a, b) = (a, b + 1)
            elif (a - 1, b + 1) not in grid:
                (a, b) = (a - 1, b + 1)
            elif (a + 1, b + 1) not in grid:
                (a, b) = (a + 1, b + 1)
            else:
                keep_falling = False
            if b == void and grain_void_count is None:
                grain_void_count = grain_count - 1
            if not keep_falling:
                grid.add((a, b))
            if b == 0:
                keep_flowing = False
    return grain_void_count, grain_count


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    solve_1, solve_2 = solve(input_values)
    solve_duration = time.time() - start_time

    start_time = time.time()
    print(f"Part 1: {str(solve_1):<30}{'(':>30}{solve_duration:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2):<30}{'(':>30}{solve_duration:.3f}s)")

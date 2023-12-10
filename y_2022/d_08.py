import time
import aoc.utils as aocu
from math import prod


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [aocu.s2i(t) for t in line]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


def views(grid, x, y):
    yd = len(grid)
    xd = len(grid[0])
    left = (grid[y][xx] for xx in range(x - 1, -1, -1))
    right = (grid[y][xx] for xx in range(x + 1, xd))
    up = (grid[yy][x] for yy in range(y - 1, -1, -1))
    down = (grid[yy][x] for yy in range(y + 1, yd))
    return left, right, up, down


def visible(grid, x, y):
    h = grid[y][x]
    return any(all(hh < h for hh in direction) for direction in views(grid, x, y))


def scenic_score(grid, x, y):
    h = grid[y][x]
    d_scores = []
    for direction in views(grid, x, y):
        d_score = 0
        for hh in direction:
            d_score += 1
            if hh >= h:
                break
        d_scores.append(d_score)
    return prod(d_scores)


def solve_1(grid):
    yd = len(grid)
    xd = len(grid[0])
    count = 0
    for x in range(0, xd):
        for y in range(0, yd):
            count += visible(grid, x, y)
    return count


def solve_2(grid):
    yd = len(grid)
    xd = len(grid[0])
    maxv = 0
    for x in range(0, xd):
        for y in range(0, yd):
            maxv = max(maxv, scenic_score(grid, x, y))
    return maxv


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

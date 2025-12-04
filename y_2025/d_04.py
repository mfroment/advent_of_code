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
            tokens = [list(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def count_local_rolls(grid, x, y):
    res = 0
    for xn in range(max(x-1,0),min(x+2,len(grid[0]))):
        for yn in range(max(y-1,0),min(y+2,len(grid))):
            if grid[yn][xn] == '@':
                res += 1
    return res


def solve_1(grid):
    res = 0
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x]=='@':
                if count_local_rolls(grid, x, y) <= 4:
                    res +=1
    return res


def solve_2(inp_grid):
    grid = inp_grid[:]
    removed = 0
    while True:
        removable = set()
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if grid[y][x]=='@':
                    if count_local_rolls(grid, x, y) <= 4:
                        removable.add((x,y))
        if len(removable) == 0:
            break
        else:
            removed += len(removable)
            for x, y in removable:
                grid[y][x]='x'
    return removed


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

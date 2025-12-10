import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = list(line)
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


# no time to write proper, clever code today for either part
# so I just brute forced it


def find_vertical_reflections(grid, exclude=None):
    for i in range(1, len(grid[0])):
        match = True
        for v in grid:
            ls = "".join(reversed(v[:i]))
            rs = "".join(v[i:])
            if not ls.startswith(rs) and not rs.startswith(ls):
                match = False
                break
        if match and i != exclude:
            return i
    return None


def transpose(grid):
    return list(map(list, zip(*grid)))


def find_reflections_in_grid(grid, exclude_v=None, exclude_h=None):
    res_v = find_vertical_reflections(grid, exclude_v)
    res_h = find_vertical_reflections(transpose(grid), exclude_h)
    return res_v, res_h


def find_reflections_in_smudged(grid):
    res_v0, res_h0 = find_reflections_in_grid(grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = "#" if grid[i][j] == "." else "."
            res_v, res_h = find_reflections_in_grid(grid, res_v0, res_h0)
            if res_v:
                return res_v, None
            elif res_h:
                return None, res_h
            grid[i][j] = "#" if grid[i][j] == "." else "."
    assert False  # should never happen with the input


def solve(values, find_reflections_function):
    score = 0
    for grid in values:
        res_v, res_h = find_reflections_function(grid)
        score += (res_v if res_v else 0) + 100 * (res_h if res_h else 0)
    return score


def solve_1(values):
    return solve(values, find_reflections_in_grid)


def solve_2(values):
    return solve(values, find_reflections_in_smudged)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

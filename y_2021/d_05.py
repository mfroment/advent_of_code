from pathlib import Path
import re


def parse_input(file=__file__):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        for r in f.readlines():
            m = re.search(r'(\d+),(\d+) -> (\d+),(\d+)', r)
            line = ([int(m.group(x)) for x in range(1, 5)])
            res.append(line)
    return res


def make_landscape(lines):
    max_x = 0
    max_y = 0
    for l in lines:
        max_x = max(max_x, l[0], l[2])
        max_y = max(max_y, l[1], l[3])
    return [[0] * (max_x + 1) for _ in range(max_y + 1)]


def solve(lines, line_validation, threshold):
    landscape = make_landscape(lines)
    count = 0
    for l in lines:
        if line_validation(l):
            x_inc = 0 if l[0] == l[2] else 1 if l[0] < l[2] else -1
            y_inc = 0 if l[1] == l[3] else 1 if l[1] < l[3] else -1
        else:
            continue
        x, y = l[0] - x_inc, l[1] - y_inc
        while not (x == l[2] and y == l[3]):
            x += x_inc
            y += y_inc
            landscape[y][x] += 1
            if landscape[y][x] == threshold:
                count += 1
    return count


def solve_1(lines):
    return solve(lines, lambda l: l[0] == l[2] or l[1] == l[3], 2)


def solve_2(lines):
    return solve(lines, lambda l: l[0] == l[2] or l[1] == l[3] or abs(l[2] - l[0]) == abs(l[3] - l[1]), 2)


if __name__ == "__main__":
    input_lines = parse_input()

    print("Part 1:", solve_1(input_lines))
    print("Part 2:", solve_2(input_lines))

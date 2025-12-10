from pathlib import Path
from numpy import prod


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for r in f.readlines():
            if r == "":
                continue
            res.append([0 if v == "." else 1 for v in r.strip()])
        return res


def solve_1(values, r, d):
    sx, sy = len(values[0]), len(values)
    x, y = 0, 0
    n = 0
    while y + d < sy:
        x, y = (x + r) % sx, y + d
        n += values[y][x]
    return n


def solve_2(values, slopes):
    return prod([solve_1(values, r, d) for (r, d) in slopes])


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values, 3, 1))
    print("Part 2:", solve_2(input_values, ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))))

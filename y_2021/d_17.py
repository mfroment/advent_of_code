from pathlib import Path
import re
from math import isqrt


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        r = f.readline().strip()
        m = re.search("target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", r)
        return [int(m.group(i)) for i in range(1, 5)]


def solve_1(values):
    xl, xu, yl, yu = values
    vxl, vxu, vyl, vyu = isqrt(2 * xl) - 1, xu, yl, -yl
    res = 0
    for vx0 in range(vxl, vxu + 1):
        for vy0 in range(vyl, vyu + 1):
            x, y, vx, vy = 0, 0, vx0, vy0
            maxy = 0
            while y >= yl and x <= xu:
                maxy = max(y, maxy)
                if xl <= x <= xu and yl <= y <= yu:
                    if maxy > res:
                        res = maxy
                        break
                x, y, vy, vx = x + vx, y + vy, vy - 1, max(0, vx - 1)
    return res


def solve_2(values):
    xl, xu, yl, yu = values
    vxl, vxu, vyl, vyu = isqrt(2 * xl) - 1, xu, yl, -yl
    res = 0
    for vx0 in range(vxl, vxu + 1):
        for vy0 in range(vyl, vyu + 1):
            x, y, vx, vy = 0, 0, vx0, vy0
            while y >= yl and x <= xu:
                if xl <= x <= xu and yl <= y <= yu:
                    res += 1
                    break
                x, y, vy, vx = x + vx, y + vy, vy - 1, max(0, vx - 1)
    return res


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

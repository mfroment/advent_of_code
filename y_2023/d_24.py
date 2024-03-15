import re
import time

import z3

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for line in sections[0]:
        px, py, pz, dx, dy, dz = tuple(
            int(e)
            for e in re.search(
                r"(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*@\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)", line
            ).groups()
        )
        res.append((px, py, pz, dx, dy, dz))
    return res  # dimensionality reduction


def intersect_lines(x1, y1, vx1, vy1, x2, y2, vx2, vy2, future=True):
    det = vx2 * vy1 - vx1 * vy2
    if det == 0:
        return None, None, None, None
    else:
        t1 = -(vy2 * (x2 - x1) - vx2 * (y2 - y1)) / det
        t2 = -(vy1 * (x2 - x1) - vx1 * (y2 - y1)) / det
        x = x1 + vx1 * t1
        y = y1 + vy1 * t1
        return x, y, t1, t2


def solve_1(values, lb=200000000000000, ub=400000000000000):
    n = 0
    for i in range(len(values) - 1):
        x1, y1, vx1, vy1 = values[i][0], values[i][1], values[i][3], values[i][4]
        for j in range(i + 1, len(values)):
            x2, y2, vx2, vy2 = values[j][0], values[j][1], values[j][3], values[j][4]
            x, y, t1, t2 = intersect_lines(x1, y1, vx1, vy1, x2, y2, vx2, vy2)
            if x is not None and t1 >= 0 and t2 >= 0 and lb <= x <= ub and lb <= y <= ub:
                n += 1
    return n


def line_relation(x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2):
    # result = identical, parallel, coplanar, skew
    colinear = vx1 * vy2 == vx2 * vy1 and vy1 * vz2 == vy2 * vz1 and vz1 * vx2 == vz2 * vx1
    # if colinear, the lines are either identical if they "intersect" or strictly parallel
    if colinear:
        identical = (
            (x1 - x2) * vy1 == (y1 - y2) * vx1
            and (y1 - y2) * vz1 == (z1 - z2) * vy1
            and (z1 - z2) * vx1 == (x1 - x2) * vz1
        )
        return "identical" if identical else "parallel"
    # if not parallel, the lines are either coplanar if they intersect or skew if they don't
    else:
        delta = (x1 - x2, y1 - y2, z1 - z2)
        cross = (vx1 * vy2 - vx2 * vy1, vy1 * vz2 - vy2 * vz1, vz1 * vx2 - vz2 * vx1)
        dotprod = delta[0] * cross[0] + delta[1] * cross[1] + delta[2] * cross[2]
        return "coplanar" if dotprod == 0 else "skew"


def solve_2(values):
    # So if 2 lines were coplanar (parallel or intersecting, not identical), we could then look at the intersections of other lines
    # with the implied plane, which would give us the rock's position and velocity with manageable maths.
    for i in range(len(values) - 1):
        x1, y1, z1, vx1, vy1, vz1 = values[i]
        for j in range(i + 1, len(values)):
            x2, y2, z2, vx2, vy2, vz2 = values[j]
            if line_relation(x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2) != "skew":
                print(f"Found 2 non-skew lines: {i} and {j}")

    # But that's not the case for that input. All pairs are skew.
    # According to https://www.quora.com/Given-four-skew-lines-how-many-lines-intersect-all-of-them ,
    # given 4 skew lines, there are either 0, 1, 2 or infinitely many lines crossing all 4 of them depending on the configuration.

    # We know there's at least 1 line crossing all 4 of them. Leap of faith: there's only 1. (with 4 lines and given the
    # existence and unicity of the answer, it seems plausible that there's 1 or 2 for any pick of 4 lines; which would be
    # likely resolved by adding a 5th line ; but using 4, 5, 6 and getting the same answer, I found out we don't need to:)
    s = z3.Solver()
    px, py, pz, vx, vy, vz = z3.Ints("px py pz vx vy vz")
    tis = []
    for i in range(4):
        pxi, pyi, pzi, vxi, vyi, vzi = values[i]
        ti = z3.Int(f"t{i}")
        tis.append(ti)
        s.add(pxi + vxi * ti == px + vx * ti)
        s.add(pyi + vyi * ti == py + vy * ti)
        s.add(pzi + vzi * ti == pz + vz * ti)
        s.add(ti >= 0)
    assert s.check() == z3.sat
    m = s.model()
    return m[px].as_long() + m[py].as_long() + m[pz].as_long()


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

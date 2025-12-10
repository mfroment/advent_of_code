from pathlib import Path
import re
from itertools import product
import time


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for r in f.readlines():
            if r == "":
                continue
            m = re.search(r"(on|off) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)", r.strip())
            res.append([1 if m.group(1) == "on" else 0] + [int(m.group(i)) for i in range(2, 8)])
        return res


def solve_1(values):
    state = set()
    for s, x0, x1, y0, y1, z0, z1 in values:
        if x0 < -50 or x1 > 50 or y0 < -50 or y1 > 50 or z0 < -50 or z1 > 50:
            continue
        for x, y, z in product(range(x0, x1 + 1), range(y0, y1 + 1), range(z0, z1 + 1)):
            if s == 0 and (x, y, z) in state:
                state.remove((x, y, z))
            elif s == 1:
                state.add((x, y, z))
    return len(state)


class Cube:
    def __init__(self, xs, ys, zs):
        self.xs = xs
        self.ys = ys
        self.zs = zs

    def intersect(self, c):
        xs = Cube.overlap(self.xs, c.xs)
        ys = Cube.overlap(self.ys, c.ys)
        zs = Cube.overlap(self.zs, c.zs)
        if xs is None or ys is None or zs is None:
            return None
        else:
            return Cube(xs, ys, zs)

    def clip(self, c):
        ic = self.intersect(c)
        if ic is None:
            return [self]
        else:
            xss = [
                (self.xs[0], ic.xs[0] - 1),
                (ic.xs[0], ic.xs[1]),
                (ic.xs[1] + 1, self.xs[1]),
            ]
            yss = [
                (self.ys[0], ic.ys[0] - 1),
                (ic.ys[0], ic.ys[1]),
                (ic.ys[1] + 1, self.ys[1]),
            ]
            zss = [
                (self.zs[0], ic.zs[0] - 1),
                (ic.zs[0], ic.zs[1]),
                (ic.zs[1] + 1, self.zs[1]),
            ]
            sub_cs = []
            for i, ess in enumerate(product(xss, yss, zss)):
                if i == 13:  # the central cuboid is the one that's clipped
                    continue
                nxs, nys, nzs = ess
                if nxs[0] > nxs[1] or nys[0] > nys[1] or nzs[0] > nzs[1]:
                    continue
                sub_cs.append(Cube(nxs, nys, nzs))
            return sub_cs

    def count(self):
        return (self.xs[1] - self.xs[0] + 1) * (self.ys[1] - self.ys[0] + 1) * (self.zs[1] - self.zs[0] + 1)

    @staticmethod
    def overlap(ps, qs):
        rs = (max(ps[0], qs[0]), min(ps[1], qs[1]))
        return rs if rs[0] <= rs[1] else None


def solve_2(values):
    total = 0
    for i, (s, x0, x1, y0, y1, z0, z1) in enumerate(values):
        if s == 0:
            continue
        cubes = [Cube((x0, x1), (y0, y1), (z0, z1))]
        for j, (_, xx0, xx1, yy0, yy1, zz0, zz1) in enumerate(values[i + 1 :]):
            nc = Cube((xx0, xx1), (yy0, yy1), (zz0, zz1))
            ncubes = []
            for c in cubes:
                ncubes += c.clip(nc)
            cubes = ncubes
        total += sum([c.count() for c in cubes])
    return total


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {solve_1(input_values):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {solve_2(input_values):<30}{'(':>30}{time.time() - start_time:.3f}s)")

from pathlib import Path


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip()])
            # m = re.search(r'(..) -> (.)', r.strip())
            # insertions[m.group(1)] = m.group(2)
        return res


def nuply(values, factor):
    res = [[None] * (len(values[0]) * factor) for _ in range(len(values) * factor)]
    for j in range(len(res)):
        for i in range(len(res[0])):
            tmp = (((values[j % len(values)][i % len(values[0])] + j // len(values) + i // len(values[0])) - 1) % 9) + 1
            res[j][i] = tmp
    return res


# -- Solving the wrong problem: from top-left to bottom-right only going down & right
#    The problem description misled me into thinking that was the problem to solve. Used dynamic programming.
#    It works on the example for both part 1 & 2, and worked on my problem input for part 1 (!!!!)
#    Much time wasted on part 2.
def lowest_path_no_backtrack(g, i, j, p):
    if p[j][i] is None:
        minp = g[j][i]
        if i == 0:
            if j > 0:
                minp += lowest_path_no_backtrack(g, i, j - 1, p)
        else:
            if j == 0:
                minp += lowest_path_no_backtrack(g, i - 1, j, p)
            else:
                minp += min(lowest_path_no_backtrack(g, i, j - 1, p), lowest_path_no_backtrack(g, i - 1, j, p))
        p[j][i] = minp
    return p[j][i]


# -- Solving the correct problem - Clunky version.
#    "It's a mess, but it's my mess."
#    Implement Dijkstra without a proper priority queue (used 2 distance storage instead, one with all values,
#    the other updated to pluck out the decided values, so it's slightly faster to look the next one up).
#    It's slow but completes eventually (after 30s or so on MB Pro 2019).
#    Also using dicts of dicts instead of flattening into a proper graph.
#    Also variable naming shows a growing sense of urgency.
class Clunky:

    @staticmethod
    def neighbours(i, j):
        return {(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)}

    @staticmethod
    def get2(d, i, j):
        if i in d and j in d[i]:
            return d[i][j]
        else:
            return None

    @staticmethod
    def set2(d, i, j, v):
        d.setdefault(i, dict())
        d[i].setdefault(j, dict())
        d[i][j] = v

    @staticmethod
    def cl2(d, i, j):
        del d[i][j]
        if len(d[i]) == 0:
            del d[i]

    @staticmethod
    def picknext(v, d):
        mind = None
        nv = None
        for i in d:
            for j in d[i]:
                if (i, j) in v:
                    if Clunky.get2(d, i, j) is not None and (mind is None or Clunky.get2(d, i, j) < mind):
                        mind = Clunky.get2(d, i, j)
                        nv = (i, j)
        return nv, mind

    @staticmethod
    def lowest_path_2(g):
        d = dict()
        dd = dict()
        p = dict()
        v = set()
        for j in range(len(g)):
            for i in range(len(g[0])):
                v.add((i, j))
        Clunky.set2(d, 0, 0, 0)
        Clunky.set2(dd, 0, 0, 0)
        while len(v) > 0:
            nv, mind = Clunky.picknext(v, dd)
            v.remove(nv)
            Clunky.cl2(dd, nv[0], nv[1])
            for nvn in Clunky.neighbours(nv[0], nv[1]):
                if nvn in v:
                    alt = Clunky.get2(d, nv[0], nv[1]) + g[nvn[1]][nvn[0]]
                    if Clunky.get2(d, nvn[0], nvn[1]) is None or alt < Clunky.get2(d, nvn[0], nvn[1]):
                        Clunky.set2(d, nvn[0], nvn[1], alt)
                        Clunky.set2(dd, nvn[0], nvn[1], alt)
                        Clunky.set2(p, nvn[0], nvn[1], nv)
        return d, p

    @staticmethod
    def solve(values):
        p, d = Clunky.lowest_path_2(values)
        return Clunky.get2(p, len(values[0]) - 1, len(values) - 1)

    @staticmethod
    def solve_1(values):
        return Clunky.solve(values)

    @staticmethod
    def solve_2(values):
        return Clunky.solve(nuply(values, 5))


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", Clunky.solve_1(input_values))
    print("Part 2:", Clunky.solve_2(input_values))

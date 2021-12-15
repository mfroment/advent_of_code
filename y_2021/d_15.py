from pathlib import Path
import heapq


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip()])
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
class Sweep:
    @staticmethod
    def lowest_path(values):
        p = [[None] * len(values[0]) for _ in range(len(values))]
        p[0][0] = 0
        for j in range(len(values)):
            for i in range(len(values[0])):
                if i == 0 and j == 0:
                    continue
                p[j][i] = values[j][i] + min(p[j - 1][i] if j > 0 else float('inf'),
                                             p[j][i - 1] if i > 0 else float('inf'))
        return p

    @staticmethod
    def solve(values):
        return Sweep.lowest_path(values)[len(values) - 1][len(values[0]) - 1]

    @staticmethod
    def solve_1(values):
        return Sweep.solve(values)

    @staticmethod
    def solve_2(values):
        return Sweep.solve(nuply(values, 5))


# -- Solving the correct problem - Clunky version.
#    "It's a mess, but it's my mess."
#    Implement Dijkstra without a proper priority queue. Instead, used 2 distance stores, one with all values,
#    the other updated to pluck out the settled values, so that it's slightly faster to look the next one up).
#    It's slow but completes eventually (after 30s or so on MB Pro 2019).
#    Also, using dicts of dicts instead of transforming the coordinates into keys & flattening the data structures.
#    Also, the variable naming shows a growing sense of urgency.
class Clunky:
    @staticmethod
    def neighbours(i, j):
        return {(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)}

    @staticmethod
    def get_2d(d, i, j):
        return d.get(i, dict()).get(j, None)

    @staticmethod
    def set_2d(d, i, j, v):
        d.setdefault(i, dict()).setdefault(j, dict())
        d[i][j] = v

    @staticmethod
    def del_2d(d, i, j):
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
                    if Clunky.get_2d(d, i, j) is not None and (mind is None or Clunky.get_2d(d, i, j) < mind):
                        mind = Clunky.get_2d(d, i, j)
                        nv = (i, j)
        return nv, mind

    @staticmethod
    def lowest_path(g):
        d = dict()
        dd = dict()
        p = dict()
        v = set()
        for j in range(len(g)):
            for i in range(len(g[0])):
                v.add((i, j))
        Clunky.set_2d(d, 0, 0, 0)
        Clunky.set_2d(dd, 0, 0, 0)
        while len(v) > 0:
            nv, mind = Clunky.picknext(v, dd)
            v.remove(nv)
            Clunky.del_2d(dd, nv[0], nv[1])
            for nvn in Clunky.neighbours(nv[0], nv[1]):
                if nvn in v:
                    alt = Clunky.get_2d(d, nv[0], nv[1]) + g[nvn[1]][nvn[0]]
                    if Clunky.get_2d(d, nvn[0], nvn[1]) is None or alt < Clunky.get_2d(d, nvn[0], nvn[1]):
                        Clunky.set_2d(d, nvn[0], nvn[1], alt)
                        Clunky.set_2d(dd, nvn[0], nvn[1], alt)
                        Clunky.set_2d(p, nvn[0], nvn[1], nv)
        return d, p

    @staticmethod
    def solve(values):
        d, _ = Clunky.lowest_path(values)
        return Clunky.get_2d(d, len(values[0]) - 1, len(values) - 1)

    @staticmethod
    def solve_1(values):
        return Clunky.solve(values)

    @staticmethod
    def solve_2(values):
        return Clunky.solve(nuply(values, 5))


def graphify(values):
    # transform the matrix input into a weighted graph
    # (i,j) flattened into i_j
    x_size, y_size = len(values[0]), len(values)

    def neighbours(i, j):
        return {(x, y) for (x, y) in {(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)} if
                0 <= x < x_size and 0 <= y < y_size}

    def coord_to_key(i, j):
        return str(i) + '_' + str(j)

    g = dict()
    for i in range(len(values[0])):
        for j in range(len(values)):
            i_j = coord_to_key(i, j)
            for (x, y) in neighbours(i, j):
                x_y = coord_to_key(x, y)
                g.setdefault(x_y, dict())
                g[x_y][i_j] = values[j][i]
    return g


# -- Solving the correct problem - Cleaner version
#    Cleaner Dijkstra using a weighted edge graph as input.
#    A priority queue is used (heap, actually), but suboptimal (no update mechanism, instead the same node may
#    be pushed again if a shorter distance is found further on; if a node that's been marked as settled is popped
#    from the priority queue, it's discarded). Still much faster than the Clunky version.
class Cleaner:
    @staticmethod
    def lowest_path(g, src):
        # returns minimal distance & predecessors
        # src is the source node
        dist = dict()
        dist[src] = 0
        prev = dict()
        settled = set()
        pqueue = [(0, src)]
        heapq.heapify(pqueue)
        while len(pqueue) > 0:
            d, n = heapq.heappop(pqueue)
            if n in settled:
                continue  # See the remark on pushing the same node several times in the pqueue in the top comment.
            settled.add(n)
            for m, e in g[n].items():
                if m not in settled:
                    candidate = dist[n] + e
                    if m not in dist or candidate < dist[m]:
                        prev[m] = n
                        dist[m] = candidate
                        heapq.heappush(pqueue, (candidate, m))
        return prev, dist

    @staticmethod
    def solve(values):
        g = graphify(values)
        p, d = Cleaner.lowest_path(g, '0_0')
        return d[str(len(values[0]) - 1) + '_' + str(len(values) - 1)]

    @staticmethod
    def solve_1(values):
        return Cleaner.solve(values)

    @staticmethod
    def solve_2(values):
        return Cleaner.solve(nuply(values, 5))


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", Cleaner.solve_1(input_values))
    print("Part 2:", Cleaner.solve_2(input_values))

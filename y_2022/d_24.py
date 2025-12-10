import math
import time
import aoc.utils as aocu
import networkx as ntx


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [c for c in line]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


WINDS = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def pos_add_mod(p, q, w, h):
    px, py = p
    qx, qy = q
    return (px + qx - 1) % w + 1, (py + qy - 1) % h + 1


def pos_add(p, q):
    px, py = p
    qx, qy = q
    return px + qx, py + qy


def make_basin(values):
    basin = dict()
    h = len(values) - 2
    w = len(values[0]) - 2
    for y in range(1, h + 1):
        for x in range(1, w + 1):
            v = values[y][x]
            if v != ".":
                basin[(x, y)] = {WINDS[v]}
    return basin, w, h


def make_basins(basin, w, h):
    basins = [basin]
    m = math.lcm(w, h)
    for _ in range(m):
        nbasin = dict()
        for (x, y), vs in basin.items():
            for v in vs:
                nv = pos_add_mod((x, y), v, w, h)
                assert 1 <= nv[0] <= w and 1 <= nv[1] <= h
                nbasin[nv] = nbasin.get(nv, set()) | {(v)}
        basins.append(nbasin)
        basin = nbasin
    assert basins[0] == basins[-1]  # Sanity check: should loop back
    basins.pop()  # It loops back so discard the duplicate starting position
    return basins


def make_reachable(basin, w, h):
    reachable = set()
    # The 2 entry points to the basin:
    reachable.add((1, 0))
    reachable.add((w, h + 1))
    # The windy basin:
    for y in range(1, h + 1):
        for x in range(1, w + 1):
            if (x, y) not in basin:
                reachable.add((x, y))
    return reachable


def make_reachables(basins, w, h):
    reachables = []
    for basin in basins:
        reachables.append(make_reachable(basin, w, h))
    return reachables


def make_graph(reachables, w, h):
    # Node in graph = (time % cycle_length, x, y)
    G = ntx.DiGraph()
    for ri, r in enumerate(reachables):
        nri = (ri + 1) % len(reachables)
        nr = reachables[nri]
        for x, y in r:
            for dp in (0, 0), (1, 0), (-1, 0), (0, 1), (0, -1):
                nx, ny = pos_add((x, y), dp)
                if (nx, ny) in nr:
                    G.add_edge((ri, x, y), (nri, nx, ny))
        # Exit conditions = being at one entry point at any time
        G.add_edge((ri, 1, 0), "A", weight=0)
        G.add_edge((ri, w, h + 1), "B", weight=0)
    return G


def solve_1_and_2(values):
    basin, w, h = make_basin(values)
    basins = make_basins(basin, w, h)
    reachables = make_reachables(basins, w, h)
    G = make_graph(reachables, w, h)
    l_cycle = len(reachables)
    r1 = ntx.shortest_path(G, source=(0, 1, 0), target="B")
    t1 = len(r1) - 2
    r2 = ntx.shortest_path(G, source=(t1 % l_cycle, w, h + 1), target="A")
    t2 = t1 + len(r2) - 2
    r3 = ntx.shortest_path(G, source=(t2 % l_cycle, 1, 0), target="B")
    t3 = t2 + len(r3) - 2
    return t1, t2, t3


def main():
    input_values = parse_input()

    start_time = time.time()
    t1, t2, t3 = solve_1_and_2(input_values)
    print(f"t1, t2, t3 = {t1, t2, t3}")
    print(f"Part 1: {str(t1):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    print(f"Part 2: {str(t3):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

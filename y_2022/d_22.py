import time
import re
from dataclasses import dataclass
from typing import Dict, Tuple

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    raw_grid = []
    for line in sections[0]:
        raw_grid.append(line)
    moves = re.split(r"(R|L)", sections[1][0], maxsplit=0)
    moves = [aocu.s2i(t) for t in moves]
    return raw_grid, moves


# facing aliases
R, D, L, U = (1, 0), (0, 1), (-1, 0), (0, -1)

# facing "score"
FACING_VALUE = {
    R: 0,
    D: 1,
    L: 2,
    U: 3,
}

# compute new facing when turning
TURNING = {
    'L': lambda p: (p[1], -p[0]),
    'R': lambda p: (-p[1], p[0]),
}


@dataclass
class Node:
    # True -> path, False -> block
    v: bool | None
    # neighbours: dictionary, indexed by facing (R,D,L,U)
    #      with values a pair of 2-tuples : ((coordinates of the neighbour), (new facing))
    n: Dict[Tuple[int, int], Tuple[Tuple[int, int], Tuple[int, int]]]

    def __init__(self):
        self.n = dict()
        self.v = None


def make_grid_1(values):
    h = len(values)
    w = max(len(v) for v in values)

    def add_pos(p, q):
        return (p[0] + q[0]) % w, (p[1] + q[1]) % h

    nodes = dict()
    # Set values
    for j in range(h):
        for i in range(w):
            n = Node()
            if i < len(values[j]):
                v = values[j][i]
                if v == ' ':
                    continue
                n.v = (v == '.')
                nodes[(i, j)] = n
    # Set neighbours
    for p, n in nodes.items():
        for facing in R, D, L, U:
            q = p
            while q == p or q not in nodes:
                q = add_pos(q, facing)
            nodes[p].n[facing] = (q, facing)
    return nodes


def make_grid_2(values):
    # this only works for a 50x50x50 cube with the specific puzzle input layout
    nodes = make_grid_1(values)

    # "Fix" cube boundary neighbours (position + facing)
    for i in range(50):
        # Edges clockwise from top border, by pairs of connecting edges (skip if already visited)
        nodes[(50 + i, 0)].n[U] = ((0, 150 + i), R)
        nodes[(0, 150 + i)].n[L] = ((50 + i, 0), D)

        nodes[(100 + i, 0)].n[U] = ((i, 199), U)
        nodes[(i, 199)].n[D] = ((100 + i, 0), D)

        nodes[(149, i)].n[R] = ((99, 149 - i), L)
        nodes[(99, 149 - i)].n[R] = ((149, i), L)

        nodes[(100 + i, 49)].n[D] = ((99, 50 + i), L)
        nodes[(99, 50 + i)].n[R] = ((100 + i, 49), U)

        nodes[(50 + i, 149)].n[D] = ((49, 150 + i), L)
        nodes[(49, 150 + i)].n[R] = ((50 + i, 149), U)

        nodes[(0, 100 + i)].n[L] = ((50, 49 - i), R)
        nodes[(50, 49 - i)].n[L] = ((0, 100 + i), R)

        nodes[(i, 100)].n[U] = ((50, 50 + i), R)
        nodes[(50, 50 + i)].n[L] = ((i, 100), D)

    return nodes


def update_pos(p, facing, move, nodes):
    if isinstance(move, int):
        for _ in range(move):
            np, nfacing = nodes[p].n[facing]
            if not nodes[np].v:
                break
            else:
                p, facing = np, nfacing
        return p, facing
    else:
        return p, TURNING[move](facing)


def solve(raw_grid, moves, make_grid):
    nodes = make_grid(raw_grid)
    j = 0
    i = min(i for (i, j) in nodes if j == 0)
    p, facing = (i, j), R
    for m in moves:
        # print(p, facing, m)
        p, facing = update_pos(p, facing, m, nodes)
    # print(p, facing)
    i, j = p
    return 1000 * (j + 1) + 4 * (i + 1) + FACING_VALUE[facing]


def solve_1(raw_grid, moves):
    return solve(raw_grid, moves, make_grid_1)


def solve_2(raw_grid, moves):
    return solve(raw_grid, moves, make_grid_2)


def main():
    raw_grid, moves = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(raw_grid, moves)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(raw_grid, moves)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

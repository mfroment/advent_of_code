import time
from pathlib import Path

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


def make_graph(values, infinite=False):
    w, h = len(values[0]), len(values)
    g = {}
    start = None
    for j, row in enumerate(values):
        for i, val in enumerate(row):
            if val == "#":
                continue
            if val == "S":
                start = (i, j)
            g[(i, j)] = set()
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < w and 0 <= nj < h and values[nj][ni] in {".", "S"}:
                    g[(i, j)].add((di, dj))
                if infinite:
                    if ni == 0:
                        g[(i, j)].add((-1, 0))
                    if nj == 0:
                        g[(i, j)].add((0, -1))
                    if ni == w - 1:
                        g[(i, j)].add((1, 0))
                    if nj == h - 1:
                        g[(i, j)].add((0, 1))
    return start, g, w, h


def make_get_next_step(graph, w, h):
    def get_next_step(nodes):
        next_nodes = set()
        for i, j in nodes:
            for di, dj in graph[(i % w, j % h)]:
                next_nodes.add((i + di, j + dj))
        return next_nodes

    return get_next_step


def solve_1(values, steps=64):
    start, g, w, h = make_graph(values)
    get_next_step = make_get_next_step(g, w, h)
    current = (start,)
    for _ in range(steps):
        current = get_next_step(current)
    return len(current)


# Simulating for 600 steps shows that a regular pattern repeats in each filled grid and at the partially filled grid on the edges
# every time the grid is traversed, which is every N steps, where N is the size of the (square) grid.
# Sampling the number of reachable tiles every N iterations, and analyzing the values in Google Sheets (@_@)
# it can be observed that the values have 0 third derivative.
# In other words, f(x*size+y) = a[y]*x^2 + b[y]*x + c[y] (there are N different polynoms, 1 for each modulo)
# It does not look like a general property of the problem (it does not work for the test input at 5000 steps, for example),
# but it is a property of the input.
# With this strong assumption in hand, we can derive a non-general solution for the problem that works for this input:
def pre_solve_2(values):
    def get_current_state(grid, current=None, factor=1):
        current = set() if current is None else current
        w, h = len(grid[0]), len(grid)
        cgrid = [[r if r != "S" else "." for r in row * (2 * factor - 1)] for row in (grid * (2 * factor - 1))[:]]
        for ci, cj in current:
            if (-factor + 1) * w <= ci < factor * w and (-factor + 1) * h <= cj < factor * h:
                si, sj = (factor - 1) * w + ci, (factor - 1) * h + cj
                cgrid[sj][si] = "O"
        return cgrid

    start, g, w, h = make_graph(values, infinite=True)
    get_next_step = make_get_next_step(g, w, h)
    assert w == h
    grids = []
    current = (start,)
    for i in range(600):
        grids.append(get_current_state(values, current, factor=2))
        current = get_next_step(current)
    output_file = Path(__file__).parent / "input/d_21.solve_2.html"
    aocu.grids_to_vector_graphics(
        grids,
        {
            "#": ("square", "black"),
            "O": ("circle", "red"),
        },
        html=output_file,
    )
    return str(output_file.resolve().as_uri())


def solve_2(values, n_steps=26501365):
    start, g, w, h = make_graph(values, infinite=True)
    get_next_step = make_get_next_step(g, w, h)
    assert w == h
    f = []
    x, y = n_steps // w, n_steps % w
    i, current = 0, None
    while i <= 2 * w + y:
        current = (start,) if i == 0 else get_next_step(current)
        if i % w == y:
            f.append(len(current))
        i += 1
    a = (f[2] - 2 * f[1] + f[0]) // 2
    b = -3 * f[0] + 4 * f[1] - f[2]
    c = f[0]
    return a * x**2 + b * x + c


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    # start_time = time.time()
    # print(f"Part 2 (simulation): {str(pre_solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

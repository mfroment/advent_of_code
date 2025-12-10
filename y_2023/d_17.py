import time
import aoc.utils as aocu
import networkx as nx


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = list(line)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def make_graph(grid, min_d=1, max_d=3):
    w = len(grid[0])
    h = len(grid)
    g = nx.DiGraph()
    # add nodes and edges for each cell;
    #    nodes are (i, j, next_move_horizontal?)
    #    edges are (i, j, next_move_horizontal?) -> (i', j', next_move_horizontal?'), weighted by traversed nodes
    #    if next_move_horizontal? is True, then i',j' are on the same row as i,j , and from i',j' next move will be vertical
    #    conversely, if next_move_horizontal? is False, then i',j' are on the same column as i,j , and from i',j' next move will be horizontal
    for j in range(h):
        for i in range(w):
            for di, dj, horizontality in (
                (1, 0, True),
                (-1, 0, True),
                (0, 1, False),
                (0, -1, False),
            ):
                dv = 0
                for d in range(1, max_d + 1):
                    ni = i + di * d
                    nj = j + dj * d
                    if 0 <= ni < w and 0 <= nj < h:
                        dv += grid[nj][ni]
                        if d >= min_d:
                            g.add_edge(
                                (i, j, horizontality),
                                (ni, nj, not horizontality),
                                weight=dv,
                            )
                    else:
                        break
    # add start and end nodes
    for horizontality in True, False:
        g.add_edge("start", (0, 0, horizontality), weight=0)
        g.add_edge((w - 1, h - 1, horizontality), "end", weight=0)
    return g


def solve_1(values):
    g = make_graph(values)
    return nx.shortest_path_length(g, "start", "end", weight="weight", method="dijkstra")


def solve_2(values):
    g = make_graph(values, min_d=4, max_d=10)
    return nx.shortest_path_length(g, "start", "end", weight="weight", method="dijkstra")


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

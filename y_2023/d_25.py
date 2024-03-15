import re
import time

import networkx as nx

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    return [re.split(r":?\s+", line, maxsplit=0) for line in sections[0]]


def make_graph(values):
    G = nx.Graph()
    for els in values:
        n1 = els[0]
        for n2 in els[1:]:
            G.add_edge(n1, n2)
    return G


def solve_1(values):
    G = make_graph(values)
    cutting_edges = nx.minimum_edge_cut(G)
    print(f"There are {len(cutting_edges)} edges for the minimal cut: {cutting_edges}")
    for edge in cutting_edges:
        G.remove_edge(*edge)
    res = 1
    for cc in nx.connected_components(G):
        res *= len(cc)
    return res


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

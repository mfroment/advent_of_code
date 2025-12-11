import re
import time

import aoc.utils as aocu
import networkx as nx
import functools


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r": |,|-|\s+", line, maxsplit=0)
            sub_res.append(tokens)
        res.append(sub_res)
    res = aocu.reduce_input(res)  # dimensionality reduction
    # return as a dictionary
    return {r[0]: set(r[1:]) for r in res}


def make_graph(values):
    G = nx.DiGraph()
    for node, dests in values.items():
        for dest in dests:
            G.add_edge(node, dest)
    return G


def solve_1(values):
    # Brute force: enumerate all simple paths
    G = make_graph(values)
    sps = nx.all_simple_paths(G, "you", "out")
    return len(list(sps))


def solve_2(values):
    G = make_graph(values)

    # Sanity check for DP path counting to work: graph must acyclic (=> no need to track visited nodes
    # except for dac & fft). That's the only actual use for networkx functions here!
    assert nx.is_directed_acyclic_graph(G)

    @functools.cache
    def n_paths(node, visited_dac=False, visited_fft=False):
        if node == "out":
            return 1 if (visited_dac and visited_fft) else 0
        visited_dac = visited_dac or node == "dac"
        visited_fft = visited_fft or node == "fft"
        return sum(n_paths(dest, visited_dac, visited_fft) for dest in G[node])

    return n_paths("svr")


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

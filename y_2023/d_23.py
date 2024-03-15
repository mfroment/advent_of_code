import time

import networkx as nx

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    return sections[0]


def get_edges(values):
    # this extracts the (directed) weighted edges from the input
    # there's a bit of duplication with the graph construction, but it's not too bad and helps with the sanity checks

    # first find "true" nodes = start, end, and intersections
    s = (1, 0)
    e = (len(values[0]) - 2, len(values) - 1)
    nodes = {s, e}
    for j, row in enumerate(values[1:-1], 1):
        for i, v in enumerate(row[1:-1], 1):
            if v == "#":
                continue
            assert v != "#"
            neighbours = [values[j + dj][i + di] for (di, dj) in ((0, 1), (0, -1), (1, 0), (-1, 0))]
            if neighbours.count("#") < 2:
                assert (
                    v == "."
                )  # this does not have to be true, but it is for the input, and simplifies edge direction analysis
                nodes.add((i, j))
    SLOPES = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    # now populate "true" edges
    edges = dict()
    for n in nodes:
        edges[n] = dict()
        # admissible starting directions
        sds = set()
        if n == s:
            sds.add((0, 1))
        elif n == e:
            sds.add((0, -1))
        else:
            for ndi, ndj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if values[n[1] + ndj][n[0] + ndi] != "#":
                    sds.add((ndi, ndj))
        # for each starting direction, find the next node (if not dead end), length of path, and whether it is forward or backward or both
        for sdi, sdj in sds:
            lgth = 0
            forward, backward = False, False
            cdi, cdj = sdi, sdj
            cni, cnj = n
            cv = values[cnj][cni]
            dest = None
            while True:
                lgth += 1
                if cv in SLOPES:
                    if (cdi, cdj) == SLOPES[cv]:
                        forward = True
                    elif (-cdi, -cdj) == SLOPES[cv]:
                        backward = True
                    else:
                        assert False
                nni, nnj = cni + cdi, cnj + cdj
                nv = values[nnj][nni]
                assert nv != "#"
                if (nni, nnj) in nodes:
                    dest = (nni, nnj)
                    break
                decided = False
                for ndi, ndj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    tnni, tnnj = nni + ndi, nnj + ndj
                    tnv = values[tnnj][tnni]
                    if (tnni, tnnj) != (cni, cnj) and tnv != "#":
                        decided = True
                        break
                if not decided:
                    break  # dead end
                cv = nv
                cni, cnj = nni, nnj
                cdi, cdj = ndi, ndj
            if dest:
                edges[n][dest] = (lgth, forward, backward)
    # sanity check: if an edge exists between two nodes, the opposite edge must exist as well
    for n1, n2_edges in edges.items():
        for n2, (lgth, forward, backward) in n2_edges.items():
            assert n1 in edges[n2]
            assert edges[n2][n1] == (lgth, backward, forward)
    # finally add named nodes for start and end
    edges["start"] = {s: (0, True, False)}
    edges[s] |= {"start": (0, False, True)}
    edges["end"] = {e: (0, False, True)}
    edges[e] |= {"end": (0, True, False)}

    return edges


def get_digraph(edges):
    G = nx.DiGraph()
    for n1, n2_edges in edges.items():
        for n2, (l, forward, backward) in n2_edges.items():
            if forward and not backward:  # only add purely forward edges, others if any cannot be traversed
                G.add_edge(n1, n2, length=l)
    return G


def get_bigraph(edges):
    G = nx.Graph()
    for n1, n2_edges in edges.items():
        for n2, (l, _, _) in n2_edges.items():
            if (n1, n2) not in G.edges:
                G.add_edge(n1, n2, length=l)
    return G


def solve_1(values):
    # Use longest path in a DAG = shortest path in a DAG with opposite edge lengths
    #  - technically we don't know (yet) if there's no cycle, but the algorithm would fail if there is - and there isn't!
    edges = get_edges(values)
    G = get_digraph(edges)
    return -nx.shortest_path_length(G, "start", "end", weight=lambda u, v, d: -d["length"], method="bellman-ford")


def solve_2(values):
    # We've already done the hard work for part 1 by finding the "true" edges.
    # Let's get all paths and find the longest one - it's not efficient but it's fast enough.
    edges = get_edges(values)
    G = get_bigraph(edges)
    return max(nx.path_weight(G, p, weight="length") for p in nx.all_simple_paths(G, "start", "end"))


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

import time
import re
import itertools as it

import aoc.utils as aocu
import networkx as nx


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    tunnels = dict()
    flows = dict()
    for section in sections:
        for line in section:
            tokens = re.search(r"^Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)$", line).groups()
            tokens = [aocu.s2i(t) for t in tokens]
            tunnels[tokens[0]] = set(re.split(r",\s+", tokens[2], maxsplit=0))
            flows[tokens[0]] = tokens[1]
    return tunnels, flows


def get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve):
    # First get all pairs shortest paths.
    G = nx.Graph()
    for src, tgts in tunnels.items():
        for tgt in tgts:
            nx.add_path(G, [src, tgt])
    path_lengths = dict(nx.all_pairs_shortest_path_length(G))
    # Then reduce to keep only the starting node and non-zero flow valves.
    dels = set()
    for src in path_lengths:
        if src != start_valve and flows[src] == 0:
            dels.add(src)
    for src in dels:
        del path_lengths[src]
    for src, tgts in path_lengths.items():
        dels = set()
        for tgt in tgts:
            if flows[tgt] == 0 or tgt == src:
                dels.add(tgt)
        for tgt in dels:
            del tgts[tgt]
    return path_lengths


def get_plans_solo(path_lengths, flows, journey, plans):
    # journey is (s, t, v, n) ; plans is { v: max(s for past v's) }
    s, t, v, n = journey
    plans[v] = max(plans.get(v, s), s)
    visited = set(v)
    for next_node, ttd in path_lengths[n].items():
        if next_node not in visited and ttd + 1 < t:
            new_t = t - ttd - 1
            new_s = s + flows[next_node] * new_t
            new_n = next_node
            new_v = tuple(sorted(v + (next_node,)))
            new_journey = (new_s, new_t, new_v, new_n)
            get_plans_solo(path_lengths, flows, new_journey, plans)


def solve_1(tunnels, flows):
    start_valve = 'AA'
    # Get shortest paths between valves of interest
    path_lengths = get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve)
    # Compute all possible plans:
    # A journey is a tuple with following values:
    #  s: "score" aka total pressure released by visited valves when the time runs out
    #  t: remaining time
    #  v: visited non-zero valves, in sorted order
    #  n: current location
    # Plans are a dictionary of visited non-zero valves with best score recorded for them at any point
    start_point = (0, 30, tuple(), 'AA')
    plans = dict()
    get_plans_solo(path_lengths, flows, start_point, plans)
    return max(plans.values())


def get_plans_duo(path_lengths, flows, journey, plans):
    # journey is (s, t, v, r1, r2, n1, n2) ; plans is { v: max(s for past v's) }
    s, t, v, r1, r2, n1, n2 = journey
    plans[v] = max(plans.get(v, s), s)
    if r1 is None and r2 is None:
        # end of path
        return
    assert (r1 == 0 or r2 == 0)
    visited = set(v)
    if r1 == 0:
        end_of_path = True
        for next_node, ttd in path_lengths[n1].items():
            if next_node not in visited and ttd + 1 < t:
                end_of_path = False
                time_skip = ttd + 1 if r2 is None else min(ttd + 1, r2)
                new_t = t - time_skip
                new_s = s + flows[next_node] * (t - ttd - 1)
                new_v = tuple(sorted(v + (next_node,)))
                new_r1 = ttd + 1 - time_skip
                new_r2 = None if r2 is None else (r2 - time_skip)
                new_n1 = next_node
                new_n2 = n2
                new_journey = (new_s, new_t, new_v, new_r1, new_r2, new_n1, new_n2)
                get_plans_duo(path_lengths, flows, new_journey, plans)
        if end_of_path:
            r1 = None
            # This is the end of the journey for this part of the duo. How about the other?
            if r2 is not None:
                t -= r2
                r2 = 0
            new_journey = (s, t, v, r1, r2, n1, n2)
            get_plans_duo(path_lengths, flows, new_journey, plans)
    elif r2 == 0:
        # just flip team members 1 & 2
        new_journey = (s, t, v, r2, r1, n2, n1)
        get_plans_duo(path_lengths, flows, new_journey, plans)
    else:  # Unreachable
        assert False


def solve_2_duo_journey(tunnels, flows):
    start_valve = 'AA'
    # Get shortest paths between valves of interest
    path_lengths = get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve)
    # Compute all possible plans:
    # A plan's state (complete or not) is a tuple with following values:
    #  s: "score" aka total pressure released by visited valves when the time runs out
    #  t: remaining time
    #  v: visited non-zero valves, in sorted order
    #  r1: member 1's time remaining until next destination
    #  n1: member 1's current location (if r1 == 0) or destination (if r1 > 0)
    #  r2: member 2's time remaining until next destination
    #  n1: member 1's current location (if r2 == 0) or destination (if r2 > 0)
    start_point = (0, 26, tuple(), 0, 0, 'AA', 'AA')
    plans = dict()
    get_plans_duo(path_lengths, flows, start_point, plans)
    return max(plans.values())


def solve_2_disjoint_subsets(tunnels, flows):
    start_valve = 'AA'
    # Get shortest paths between valves of interest
    path_lengths = get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve)
    # Compute all possible plans (score, time, visited_nodes) for time = 26
    start_journey = (0, 26, tuple(), 'AA')
    plans = dict()
    get_plans_solo(path_lengths, flows, start_journey, plans)
    # Now let's find the max score that is the sum of 2 scores with no common node
    plans_pairs = it.combinations(plans.items(), 2)
    best = 0
    for cpp in plans_pairs:
        (n1, s1), (n2, s2) = cpp
        if len(set(n1 + n2)) == len(n1) + len(n2):
            best = max(best, s1 + s2)
    return best


solve_2 = solve_2_disjoint_subsets


def main():
    tunnels, flows = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(tunnels, flows)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(tunnels, flows)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

import time
import re
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


def get_plans_solo(path_lengths, flows, plans):
    # plans are {'s': ... , 't': ... , 'n': [...] }
    res = []
    visited = set(plans['n'])
    for next_node, ttd in path_lengths[plans['n'][-1]].items():
        if next_node not in visited and ttd + 1 < plans['t']:
            new_t = plans['t'] - ttd - 1
            new_s = plans['s'] + flows[next_node] * new_t
            new_n = plans['n'] + [next_node]
            new_plan = {'s': new_s, 't': new_t, 'n': new_n}
            res += get_plans_solo(path_lengths, flows, new_plan)
    if len(res) == 0:
        # This is the end of the journey
        res = [plans]
    return res


def solve_1(tunnels, flows):
    start_valve = 'AA'
    # Get shortest paths between valves of interest
    path_lengths = get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve)
    # Compute all possible plans:
    # A plan's state (complete or not) is a dict with following keys:
    #  s: "score" aka total pressure released by visited valves when the time runs out
    #  t: remaining time
    #  n: visited valves, in order of visit
    start_plan = {'s': 0, 't': 30, 'n': ['AA']}
    plans = get_plans_solo(path_lengths, flows, start_plan)
    return max(c['s'] for c in plans)


def get_plans_duo(path_lengths, flows, plans):
    # {'s': ..., 't': ..., 'r1': ..., 'r2': ..., 'n1': [...], 'n2': [...] }
    res = []
    assert (plans['r1'] == 0 or plans['r2'] == 0)
    visited = set(plans['n1'] + plans['n2'])
    # TODO: make that DRY:
    if plans['r1'] == 0:
        for next_node, ttd in path_lengths[plans['n1'][-1]].items():
            if next_node not in visited and ttd + 1 < plans['t']:
                time_skip = ttd + 1 if plans['r2'] is None else min(ttd + 1, plans['r2'])
                new_t = plans['t'] - time_skip
                new_s = plans['s'] + flows[next_node] * (plans['t'] - ttd - 1)
                new_r1 = ttd + 1 - time_skip
                new_r2 = None if plans['r2'] is None else (plans['r2'] - time_skip)
                new_n1 = plans['n1'] + [next_node]
                new_n2 = plans['n2'][:]
                new_plan = {'s': new_s, 't': new_t, 'r1': new_r1, 'r2': new_r2, 'n1': new_n1, 'n2': new_n2}
                res += get_plans_duo(path_lengths, flows, new_plan)
        if len(res) == 0:
            plans['r1'] = None
            # This is the end of the journey for this member. How about the other?
            if plans['r2'] is not None:
                plans['t'] -= plans['r2']
                plans['r2'] = 0
                res = get_plans_duo(path_lengths, flows, plans)
            else:
                res = [plans]
        return res
    elif plans['r2'] == 0:
        for next_node, ttd in path_lengths[plans['n2'][-1]].items():
            if next_node not in visited and ttd + 1 < plans['t']:
                time_skip = ttd + 1 if plans['r1'] is None else min(ttd + 1, plans['r1'])
                new_t = plans['t'] - time_skip
                new_s = plans['s'] + flows[next_node] * (plans['t'] - ttd - 1)
                new_r2 = ttd + 1 - time_skip
                new_r1 = None if plans['r1'] is None else (plans['r1'] - time_skip)
                new_n2 = plans['n2'] + [next_node]
                new_n1 = plans['n1'][:]
                new_plan = {'s': new_s, 't': new_t, 'r1': new_r1, 'r2': new_r2, 'n1': new_n1, 'n2': new_n2}
                res += get_plans_duo(path_lengths, flows, new_plan)
        if len(res) == 0:
            plans['r2'] = None
            # This is the end of the journey for this member. How about the other?
            if plans['r1'] is not None:
                plans['t'] -= plans['r1']
                plans['r1'] = 0
                res = get_plans_duo(path_lengths, flows, plans)
            else:
                res = [plans]
        return res
    # Unreachable
    assert False


def solve_2(tunnels, flows):
    start_valve = 'AA'
    # Get shortest paths between valves of interest
    path_lengths = get_all_valve_pairs_shortest_paths(tunnels, flows, start_valve)
    # Compute all possible plans:
    # A plan's state (complete or not) is a dict with following keys:
    #  s: "score" aka total pressure released by visited valves when the time runs out
    #  t: remaining time
    #  r1: member 1's time remaining until next destination
    #  n1: member 1's visited (+ next if r not 0) valves, in order of visit
    #  r2: member 2's time remaining until next destination
    #  n2: member 2's visited (+ next if r not 0) valves, in order of visit
    start_plan = {'s': 0, 't': 26, 'r1': 0, 'r2': 0, 'n1': ['AA'], 'n2': ['AA']}
    plans = get_plans_duo(path_lengths, flows, start_plan)
    return max(c['s'] for c in plans)



if __name__ == "__main__":
    tunnels, flows = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(tunnels, flows)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(tunnels, flows)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

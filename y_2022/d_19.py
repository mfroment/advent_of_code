# import concurrent.futures
import time
import re
import aoc.utils as aocu
import math


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.search(
                r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$",
                line,
            ).groups()
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def harvest_materials(*state):
    (ror, rcl, rob, rge, nor, ncl, nob, nge) = state
    nor += ror
    ncl += rcl
    nob += rob
    nge += rge
    return ror, rcl, rob, rge, nor, ncl, nob, nge


def next_states(blueprint, state):
    _, ror_or, rcl_or, rob_or, rob_cl, rge_or, rge_ob = blueprint
    res = set()
    # Note: No greedy heuristics for making robots ASAP, it does not work on the test data.
    #       On the other hand stop building robots if the existing ones harvest more resources
    #       of one kind that can be use on building anything (not applicable to geodes).
    # 1. create a rge
    ror, rcl, rob, rge, nor, ncl, nob, nge = state
    if nor >= rob_or and nob >= rge_ob:
        nor -= rge_or
        nob -= rge_ob
        ror, rcl, rob, rge, nor, ncl, nob, nge = harvest_materials(ror, rcl, rob, rge, nor, ncl, nob, nge)
        ns = (ror, rcl, rob, rge + 1, nor, ncl, nob, nge)
        res.add(ns)
    # 2. create a rob
    ror, rcl, rob, rge, nor, ncl, nob, nge = state
    if (nor >= rob_or and ncl >= rob_cl) and (rob < rge_ob):  # (can build) and (makes sense to build)
        nor -= rob_or
        ncl -= rob_cl
        ror, rcl, rob, rge, nor, ncl, nob, nge = harvest_materials(ror, rcl, rob, rge, nor, ncl, nob, nge)
        ns = (ror, rcl, rob + 1, rge, nor, ncl, nob, nge)
        res.add(ns)
    # 3. create a rcl
    ror, rcl, rob, rge, nor, ncl, nob, nge = state
    if (nor >= rcl_or) and (rcl < rob_cl):  # (can build) and (makes sense to build)
        nor -= rcl_or
        ror, rcl, rob, rge, nor, ncl, nob, nge = harvest_materials(ror, rcl, rob, rge, nor, ncl, nob, nge)
        ns = (ror, rcl + 1, rob, rge, nor, ncl, nob, nge)
        res.add(ns)
    # 4. create a ror
    ror, rcl, rob, rge, nor, ncl, nob, nge = state
    if (nor >= ror_or) and (ror < max(ror_or, rcl_or, rob_or, rge_or)):  # (can build) and (makes sense to build)
        nor -= ror_or
        ror, rcl, rob, rge, nor, ncl, nob, nge = harvest_materials(ror, rcl, rob, rge, nor, ncl, nob, nge)
        ns = (ror + 1, rcl, rob, rge, nor, ncl, nob, nge)
        res.add(ns)
    # 5. do nothing
    ror, rcl, rob, rge, nor, ncl, nob, nge = state
    ror, rcl, rob, rge, nor, ncl, nob, nge = harvest_materials(ror, rcl, rob, rge, nor, ncl, nob, nge)
    ns = (ror, rcl, rob, rge, nor, ncl, nob, nge)
    res.add(ns)

    return res


def solve_blueprint(n_iterations, blueprint):
    b_i = blueprint[0]
    current_states = {(1, 0, 0, 0, 0, 0, 0, 0)}
    for i in range(n_iterations):
        new_states = set()
        for cs in current_states:
            new_states |= next_states(blueprint, cs)
        # Prune suboptimal new states =
        # If 2 states have the same # of robots and resources, except for 1 resource, discard the one with
        # the lower amount of resources.
        discard = set()
        or_d = dict()
        cl_d = dict()
        ob_d = dict()
        ge_d = dict()
        for cs in new_states:
            ror, rcl, rob, rge, nor, ncl, nob, nge = cs
            kor = (ror, rcl, rob, rge, ncl, nob, nge)
            kcl = (ror, rcl, rob, rge, nor, nob, nge)
            kob = (ror, rcl, rob, rge, nor, ncl, nge)
            kge = (ror, rcl, rob, rge, nor, ncl, nob)
            or_d.setdefault(kor, nor)
            cl_d.setdefault(kcl, ncl)
            ob_d.setdefault(kob, nob)
            ge_d.setdefault(kge, nge)
            if or_d[kor] > nor:
                discard.add(cs)
            elif or_d[kor] < nor:
                discard.add((ror, rcl, rob, rge, or_d[kor], ncl, nob, nge))
                or_d[kor] = nor
            if cl_d[kcl] > ncl:
                discard.add(cs)
            elif cl_d[kcl] < ncl:
                discard.add((ror, rcl, rob, rge, nor, cl_d[kcl], nob, nge))
                cl_d[kcl] = ncl
            if ob_d[kob] > nob:
                discard.add(cs)
            elif ob_d[kob] < nob:
                discard.add((ror, rcl, rob, rge, nor, ncl, ob_d[kob], nge))
                ob_d[kob] = nob
            if ge_d[kge] > nge:
                discard.add(cs)
            elif ge_d[kge] < nge:
                discard.add((ror, rcl, rob, rge, nor, ncl, nob, ge_d[kge]))
                ge_d[kge] = nge
        for cs in discard:
            new_states.remove(cs)
        current_states = new_states
        print(b_i, i, "                     ", end="\r", flush=True)
    optimum = max(nge for _, _, _, _, _, _, _, nge in current_states)
    return optimum


def solve_1(blueprints):
    nges = [solve_blueprint(24, blueprint) for blueprint in blueprints]
    return sum((i + 1) * nges[i] for i in range(len(blueprints)))


def solve_2(blueprints):
    nges = [solve_blueprint(32, blueprint) for blueprint in blueprints[:3]]
    return math.prod(nges)


def main():
    blueprints = parse_input()

    start_time = time.time()
    # [9, 0, 1, 4, 1, 10, 0, 5, 15, 3, 0, 1, 2, 0, 1, 2, 2, 8, 0, 13, 5, 7, 1, 7, 3, 1, 12, 6, 3, 1]
    print(f"Part 1: {str(solve_1(blueprints)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    # [58, 9, 21]
    print(f"Part 2: {str(solve_2(blueprints)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

import re
import time

import aoc.utils as aocu

import functools

import z3

def parse_input(file=__file__, suffix=None):
    res = []
    for line in aocu.read_input(file, suffix)[0]:
        elements = [ e[1:-1] for e in re.split(r" ", line, maxsplit=0)]
        diag = elements[0]
        wirings = tuple(tuple(aocu.s2i(t) for t in re.split(r",", e, maxsplit=0)) for e in elements[1:-1])
        jolt = tuple(aocu.s2i(c) for c in re.split(r",", elements[-1], maxsplit=0))
        res.append([diag, wirings, jolt])
    return res


def toggle(light):
    if light == '.':
        return '#'
    if light == '#':
        return '.'
    raise ValueError


def apply(diag, wiring):
    return ''.join(toggle(light) if i in wiring else light for i, light in enumerate(diag))


def configure_1(diag, wirings, currents = None):
    if currents is None:
        currents = { '.' * len(diag) }
    if diag in currents:
        return 0
    successors = set()
    for c in currents:
        for w in wirings:
            successors.add(apply(c,w))
    return 1 + configure_1(diag, wirings, successors)


def solve_1(values):
    res = 0
    for diag, wirings, _ in values:
        res += configure_1(diag, wirings)
    return res


# Naive "BFS"-like: works for test, does not scale
def configure_2_basic(jolt, wirings, currents=None):
    if currents is None:
        currents = { tuple(0 for _ in range(len(jolt))) }
    if jolt in currents:
        return 0
    followings = set()
    for c in currents:
        for w in wirings:
            successor = tuple(j+1 if i in w else j for i, j in enumerate(c))
            if any(j > jolt[i] for i, j in enumerate(successor)):
                continue
            followings.add(successor)
    return 1+configure_2_basic(jolt, wirings, followings)

# Basic backward DP: works for test, does not scale
@functools.cache
def configure_2_basicdp(jolt, wirings):
    if jolt == tuple(0 for _ in range(len(jolt))):
        return 0
    res = None
    for w in wirings:
        predecessor = tuple(j-1 if i in w else j for i, j in enumerate(jolt))
        if any(j < 0 for j in predecessor):
            continue
        candidate = configure_2_basicdp(predecessor, wirings)
        if candidate is not None and (res is None or res > candidate+1):
            res = candidate+1
    return res

# Basic backward DP with wirings pruning: works for test, does not scale
def prune_wirings(jolt, wirings):
    res = set()
    for w in wirings:
        if any(jolt[i] == 0 for i in w):
            continue
        res.add(w)
    return tuple(sorted(res))


@functools.cache
def configure_2_dp_prune(jolt, wirings):
    if jolt == tuple(0 for _ in range(len(jolt))):
        return 0
    res = None
    for w in wirings:
        predecessor = tuple(j-1 if i in w else j for i, j in enumerate(jolt))
        if any(j < 0 for j in predecessor):
            raise ValueError("wirings weren't pruned")
        candidate = configure_2_basicdp(predecessor, prune_wirings(predecessor, wirings))
        if candidate is not None and (res is None or res > candidate+1):
            res = candidate+1
    return res


# ILP, using an external library. Works...
def configure_2_ilp(jolt, wirings):
    problem = z3.Optimize()
    wps = z3.Ints(' '.join(f"w{i}" for i in range(len(wirings))))
    for wp in wps:
        problem.add(wp >= 0)

    for ij, j in enumerate(jolt):
        expr = j == z3.Sum( (1 if ij in w else 0) * wps[iw]  for iw, w in enumerate(wirings) )
        problem.add(expr)
    wp_count = z3.Sum(wp for wp in wps)
    problem.minimize(wp_count)
    assert problem.check() == z3.sat
    m = problem.model()
    return m.eval(wp_count).as_long()


def solve_2(values):
    res = 0
    for _, wirings, jolt in values:
        res += configure_2_ilp(jolt, wirings)
    return res



def main():
    input_values = parse_input()

    # print(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

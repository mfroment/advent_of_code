import time
from collections import deque
from copy import deepcopy
from math import lcm

import numpy as np

import aoc.utils as aocu

# Input visualization, select Engine = fdp
# https://dreampuf.github.io/GraphvizOnline/#digraph%20G%20%7B%0A%0A%20%20%20%20pr%20-%3E%20ql%3B%0A%20%20%20%20jg%20-%3E%20mg%3B%0A%20%20%20%20mg%20-%3E%20rx%3B%0A%20%20%20%20mq%20-%3E%20gz%2C%20nt%3B%0A%20%20%20%20db%20-%3E%20ff%2C%20dz%3B%0A%20%20%20%20dx%20-%3E%20zs%2C%20bm%3B%0A%20%20%20%20bd%20-%3E%20nt%2C%20lj%3B%0A%20%20%20%20qj%20-%3E%20hj%3B%0A%20%20%20%20xs%20-%3E%20zs%2C%20dx%3B%0A%20%20%20%20xd%20-%3E%20nt%3B%0A%20%20%20%20gb%20-%3E%20fx%2C%20th%3B%0A%20%20%20%20nt%20-%3E%20ds%2C%20hj%2C%20ht%2C%20rh%2C%20qj%3B%0A%20%20%20%20ht%20-%3E%20nt%2C%20vp%3B%0A%20%20%20%20rh%20-%3E%20mg%3B%0A%20%20%20%20sq%20-%3E%20th%2C%20cd%3B%0A%20%20%20%20tt%20-%3E%20pq%3B%0A%20%20%20%20dh%20-%3E%20sh%3B%0A%20%20%20%20rz%20-%3E%20zc%3B%0A%20%20%20%20cx%20-%3E%20xr%2C%20nt%3B%0A%20%20%20%20zq%20-%3E%20tt%2C%20th%3B%0A%20%20%20%20jm%20-%3E%20mg%3B%0A%20%20%20%20lj%20-%3E%20nt%2C%20cx%3B%0A%20%20%20%20mp%20-%3E%20ff%2C%20bq%3B%0A%20%20%20%20dz%20-%3E%20ff%2C%20gd%3B%0A%20%20%20%20fz%20-%3E%20bk%2C%20th%3B%0A%20%20%20%20hj%20-%3E%20mq%3B%0A%20%20%20%20broadcaster%20-%3E%20gb%2C%20ht%2C%20vk%2C%20zz%3B%0A%20%20%20%20zc%20-%3E%20dh%3B%0A%20%20%20%20pj%20-%3E%20xs%3B%0A%20%20%20%20bn%20-%3E%20fz%3B%0A%20%20%20%20mr%20-%3E%20bf%3B%0A%20%20%20%20mj%20-%3E%20th%2C%20sq%3B%0A%20%20%20%20gg%20-%3E%20pj%2C%20zs%3B%0A%20%20%20%20sh%20-%3E%20mr%2C%20zs%3B%0A%20%20%20%20bf%20-%3E%20zs%2C%20gg%3B%0A%20%20%20%20hf%20-%3E%20mg%3B%0A%20%20%20%20bm%20-%3E%20zs%3B%0A%20%20%20%20bk%20-%3E%20zg%3B%0A%20%20%20%20pq%20-%3E%20th%2C%20mj%3B%0A%20%20%20%20xf%20-%3E%20ff%2C%20db%3B%0A%20%20%20%20th%20-%3E%20bn%2C%20gb%2C%20tt%2C%20hf%2C%20bk%3B%0A%20%20%20%20fx%20-%3E%20th%2C%20bn%3B%0A%20%20%20%20ff%20-%3E%20vd%2C%20bq%2C%20pr%2C%20vk%2C%20ql%2C%20jm%3B%0A%20%20%20%20xr%20-%3E%20nt%2C%20xd%3B%0A%20%20%20%20bq%20-%3E%20pr%3B%0A%20%20%20%20zz%20-%3E%20rz%2C%20zs%3B%0A%20%20%20%20gz%20-%3E%20nt%2C%20ds%3B%0A%20%20%20%20zs%20-%3E%20mr%2C%20pj%2C%20zz%2C%20dh%2C%20jg%2C%20zc%2C%20rz%3B%0A%20%20%20%20vd%20-%3E%20xf%3B%0A%20%20%20%20vk%20-%3E%20mp%2C%20ff%3B%0A%20%20%20%20cv%20-%3E%20ff%3B%0A%20%20%20%20cd%20-%3E%20th%3B%0A%20%20%20%20zg%20-%3E%20th%2C%20zq%3B%0A%20%20%20%20gd%20-%3E%20ff%2C%20cv%3B%0A%20%20%20%20ql%20-%3E%20lt%3B%0A%20%20%20%20lt%20-%3E%20ff%2C%20vd%3B%0A%20%20%20%20ds%20-%3E%20bd%3B%0A%20%20%20%20vp%20-%3E%20nt%2C%20qj%3B%0A%0A%7D


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)

    graph = dict()
    flipflops = dict()
    conjunctions = dict()

    for line in sections[0]:
        src, dests = line.split(" -> ")
        dests = set(dests.split(", "))

        if src[0] == "%":
            src = src[1:]
            flipflops[src] = False
        elif src[0] == "&":
            src = src[1:]
            conjunctions[src] = {}

        graph[src] = dests

    for src, dests in graph.items():
        for dest in dests:
            if dest in conjunctions:
                conjunctions[dest][src] = False

    return graph, flipflops, conjunctions


def press_button(graph, flipflops, conjunctions):
    n_low, n_high = 0, 0
    q = deque([("button", "broadcaster", False)])
    sent_high = set()

    while q:
        src, dest, pulse = q.popleft()
        if pulse:
            n_high += 1
            sent_high.add(src)
        else:
            n_low += 1

        if dest == "broadcaster":
            next_pulse = pulse
        elif dest in flipflops and not pulse:
            flipflops[dest] = not flipflops[dest]
            next_pulse = flipflops[dest]
        elif dest in conjunctions:
            conjunctions[dest][src] = pulse
            next_pulse = not all(conjunctions[dest].values())
        else:
            next_pulse = None

        if next_pulse is not None:
            for next_dest in graph[dest]:
                q.append((dest, next_dest, next_pulse))

    return n_low, n_high, sent_high


def solve_1(values):
    graph, flipflops, conjunctions = values
    flipflops, conjunctions = deepcopy(flipflops), deepcopy(conjunctions)
    n_low, n_high = 0, 0
    for _ in range(1000):
        add_low, add_high, _ = press_button(graph, flipflops, conjunctions)
        n_low += add_low
        n_high += add_high
    return n_low * n_high


def solve_2(values):
    # Basically only works on this solution because of the specific structure of the
    # graph. It's not a general solution.
    # Find out at which button press the parents of 'mg', the parent of 'rx', first send
    # a high pulse. Then find the least common multiple of those button presses.
    # Even then, it's not guaranteed that this should work. Indeed, the parent of
    # 'rx' must have last received a high pulse from all parents. But some parents may send
    # a high pulse then a low pulse in the same button press, and while we know at that
    # button press they will all send a high pulse, we don't know if the last one received
    # from by the child from all of them will be a high pulse for all of them altogether.
    graph, flipflops, conjunctions = values
    flipflops, conjunctions = deepcopy(flipflops), deepcopy(conjunctions)
    count_presses = {k: None for k in set(conjunctions["mg"].keys())}
    n_presses = 0
    while None in count_presses.values():
        _, _, sent_high = press_button(graph, flipflops, conjunctions)
        n_presses += 1
        for k, v in count_presses.items():
            if v is None and k in sent_high:
                count_presses[k] = n_presses
    return lcm(np.prod(list(count_presses.values())))


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

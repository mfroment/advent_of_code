import re
import time

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tuple(tokens))
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def distance(p, q):
    px, py, pz = p
    qx, qy, qz = q
    return (px - qx) ** 2 + (py - qy) ** 2 + (pz - qz) ** 2


def sorted_pairs(boxes):
    res = []
    for i, p in enumerate(boxes):
        for q in boxes[i + 1 :]:
            res.append((p, q, distance(p, q)))
    return sorted(res, key=lambda item: item[2])


def solve_1(boxes, stop_at):
    pairs = sorted_pairs(boxes)
    circuits = {p: {p} for p in boxes}
    n_connections = 0
    for p, q, _ in pairs:
        if q not in circuits[p]:
            merged_circuit = circuits[p] | circuits[q]
            for b in merged_circuit:
                circuits[b] = merged_circuit
        n_connections += 1
        if n_connections == stop_at:
            break

    unique_circuits = set()
    for p in boxes:
        unique_circuits.add(tuple(sorted(list(circuits[p]))))

    sizes = sorted([len(uc) for uc in unique_circuits])

    return sizes[-3] * sizes[-2] * sizes[-1]


def solve_2(boxes):
    pairs = sorted_pairs(boxes)
    # I just copy pasted the logic from solve_1, the exit cases are different enough that unifying the code is annoying
    circuits = {p: {p} for p in boxes}
    for p, q, _ in pairs:
        if q not in circuits[p]:
            merged_circuit = circuits[p] | circuits[q]
            for b in merged_circuit:
                circuits[b] = merged_circuit
            if len(merged_circuit) == len(boxes):
                break

    return p[0] * q[0]


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values, 1000)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

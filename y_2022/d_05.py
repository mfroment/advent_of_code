import time
import re
import aoc.utils as aocu
import copy


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)

    n_pos = aocu.s2i(re.sub(r"^.*\s(\S+)\s*$", r"\1", sections[0][-1]))
    positions = {k: [] for k in range(1, n_pos + 1)}
    for r in sections[0][:-1]:
        tokens = [r[1 + 4 * i] for i in range(0, n_pos)]
        for i, v in enumerate(tokens):
            if v != ' ':
                positions[i + 1].append(v)
    for i, pos in positions.items():
        positions[i] = list(reversed(pos))

    moves = []
    for r in sections[1]:
        tokens = re.search(r"^move (.+) from (.+) to (.+)", r).groups()
        tokens = [aocu.s2i(t) for t in tokens]
        moves.append(tokens)

    return positions, moves


def process_move(positions, n, src, tgt, reverse=True):
    moved = positions[src][-n:]
    if reverse:
        moved = reversed(moved)
    positions[src] = positions[src][:-n]
    positions[tgt] += moved


def top_layer(positions):
    n_pos = max(positions.keys())
    return ''.join([positions[i][-1] for i in range(1, n_pos + 1)])


def solve_moves(positions, moves, reverse=True):
    positions = copy.deepcopy(positions)
    for n, src, tgt in moves:
        process_move(positions, n, src, tgt, reverse)
    return top_layer(positions)


def solve_1(values):
    return solve_moves(values[0], values[1], reverse=True)


def solve_2(values):
    return solve_moves(values[0], values[1], reverse=False)


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

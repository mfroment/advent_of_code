import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r"\s", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


def round_score_1(p1, p2):
    # pick    : 0 rock, 1 paper, 2 scissors
    # outcome : 0 loss, 1 draw, 2 win
    p1_picks = {'A': 0, 'B': 1, 'C': 2}
    p2_picks = {'X': 0, 'Y': 1, 'Z': 2}
    p1_pick = p1_picks[p1]
    p2_pick = p2_picks[p2]
    outcome = (p2_pick - p1_pick + 1) % 3
    score = (outcome * 3) + (p2_pick + 1)
    return score


def round_score_2(p1, p2):
    # pick    : 0 rock, 1 paper, 2 scissors
    # outcome : 0 loss, 1 draw, 2 win
    p1_picks = {'A': 0, 'B': 1, 'C': 2}
    outcomes = {'X': 0, 'Y': 1, 'Z': 2}
    p1_pick = p1_picks[p1]
    outcome = outcomes[p2]
    p2_pick = (p1_pick + outcome - 1) % 3
    score = (outcome * 3) + (p2_pick + 1)
    return score


def total_score(values, scorer):
    return sum(scorer(p1, p2) for p1, p2 in values)


def solve_1(values):
    return total_score(values, round_score_1)


def solve_2(values):
    return total_score(values, round_score_2)


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

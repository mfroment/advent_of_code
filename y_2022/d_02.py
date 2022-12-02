from pathlib import Path
import time


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([v for v in r.strip().split(' ')])
        return res


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

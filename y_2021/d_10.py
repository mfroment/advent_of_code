from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([v for v in r.strip()])
    return res


from statistics import median


ANTI_PAIRS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

CORRUPTION = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

COMPLETION = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


def parse(line):
    parsing = []
    for c in line:
        if c in set('([{<'):
            parsing.append(c)
        elif c in ANTI_PAIRS:
            if len(parsing) == 0 or ANTI_PAIRS[c] != parsing.pop():
                return False, c   # corrupted: -> False, corrupted_character
    return True, parsing  # (in)complete: -> True, remaining characters to pair


def solve_1(values):
    score = 0
    for line in values:
        status, c = parse(line)
        if not status:
            score += CORRUPTION[c]
    return score


def completion_score(remainder):
    score = 0
    for c in reversed(remainder):
        score *= 5
        score += COMPLETION[c]
    return score


def solve_2(values):
    score = []
    for line in values:
        status, c = parse(line)
        if status:
            score.append(completion_score(c))
    return median(score)


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

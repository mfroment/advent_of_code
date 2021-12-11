from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        return [int(r) for r in f.readlines() if r != '']


SUM = 2020


def solve_1(values):
    diffs = set()
    for v in values:
        if SUM - v in diffs:
            return v * (SUM - v)
        diffs.add(v)
    return None


def solve_2(values):
    for i, v in enumerate(values):
        diffs = set()
        for j in range(i + 1, len(values)):
            if SUM - v - values[j] in diffs:
                return v * values[j] * (SUM - v - values[j])
            diffs.add(values[j])
    return None


if __name__ == "__main__":
    inputs = parse_input()

    print("Part 1:", solve_1(inputs))
    print("Part 2:", solve_2(inputs))

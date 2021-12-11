from pathlib import Path


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip()])
        return res


def solve_1(values):
    return None


def solve_2(values):
    return None


if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

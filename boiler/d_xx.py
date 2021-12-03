from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        return [int(r) for r in f.readlines() if r != '']


def solve_1(s):
    return None


def solve_2(s):
    return None


if __name__ == "__main__":
    input_s = parse_input()

    print(input_s)

    print("Part 1:", solve_1(input_s))
    print("Part 2:", solve_2(input_s))

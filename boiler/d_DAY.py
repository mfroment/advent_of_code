from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        return [int(r) for r in f.readlines() if r != '']


def solve_1(values):
    return None


def solve_2(values):
    return None


if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    fishes = [0] * 9
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        for v in f.readline().split(','):
            fishes[int(v)] += 1
    return fishes


def add_one_day(fishes):
    next_fishes = fishes[1:] + [fishes[0]]
    next_fishes[6] += fishes[0]
    return next_fishes


def solve(fishes, day_count):
    for i in range(day_count):
        fishes = add_one_day(fishes)
    return sum(fishes)


if __name__ == "__main__":
    input_fishes = parse_input()

    print("Part 1:", solve(input_fishes, 80))
    print("Part 2:", solve(input_fishes, 256))

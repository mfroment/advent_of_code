from pathlib import Path
from functools import reduce


def parse_input(file=__file__):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip()])
    return res


# padding the environment with a "wall" of 9s simplifies checking out of bound conditions
def pad_matrix(values, pad_value):
    pvals = [[pad_value] * (len(values[0]) + 2)]
    for r in values:
        pvals.append([pad_value] + r + [pad_value])
    pvals.append([pad_value] * (len(values[0]) + 2))
    return pvals


# -- Part 1 --
def solve_1(values):
    pvals = pad_matrix(values, 9)
    lows = []
    for j in range(1, len(pvals) - 1):
        for i in range(1, len(pvals[0]) - 1):
            if pvals[j][i] < min(pvals[j - 1][i], pvals[j + 1][i], pvals[j][i - 1], pvals[j][i + 1]):
                lows.append(pvals[j][i])
    cost = 0
    for l in lows:
        cost += l + 1
    return cost


# -- Part 2 --
def extend_basin(basin, i, j, b):
    if basin[j][i] is not None:
        return False
    basin[j][i] = b
    for i, j in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
        extend_basin(basin, i, j, b)
    return True


def extract_basins(values):
    pvals = pad_matrix(values, 9)
    basins = []
    for r in pvals:
        basins.append([-1 if v == 9 else None for v in r])
    b = 0
    for j in range(len(basins)):
        for i in range(len(basins[0])):
            if extend_basin(basins, i, j, b):
                b += 1
    return basins


def measure_basins(basins):
    sizes = dict()
    for r in basins:
        for v in r:
            if v >= 0:
                sizes.setdefault(v, 0)
                sizes[v] += 1
    return sorted(sizes.values())


def solve_2(values):
    basins = extract_basins(values)
    sizes = measure_basins(basins)
    return reduce(lambda x, y: x * y, sizes[-3:])


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

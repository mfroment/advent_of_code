from pathlib import Path
import itertools
import copy
from functools import reduce


def parse_input(file=__file__, extension=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if extension is None else '.' + extension))) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip()])
        return res


def apply_incs(grid, incs, force=False):
    # Apply energy increases to octopuses, trigger flash if applicable, compute next set of energy increases.
    # Octopuses who have 0 energy are presumed having flashed in this step and their energy is not increased,
    # unless the force flag is True ; this is used to apply the initial global 1 energy increment.
    # Increment octopuses' energy
    for j, r in enumerate(grid):
        for i, _ in enumerate(r):
            if grid[j][i] != 0 or force:
                grid[j][i] += incs[j][i]
            incs[j][i] = 0
    # Detect flash events, relax energy and compute energy increases for neighbors for the next step
    final = True
    for j, r in enumerate(grid):
        for i, _ in enumerate(r):
            if grid[j][i] >= 10:
                # Flash! Reset energy
                grid[j][i] = 0
                # Select neighbors
                ys = {max(0, j - 1), j, min(j + 1, len(grid) - 1)}
                xs = {max(0, i - 1), i, min(i + 1, len(grid[0]) - 1)}
                pos = {(x, y) for x, y in itertools.product(xs, ys) if (x, y) != (i, j)}
                # Update energy increment for neighbors
                for x, y in pos:
                    if grid[y][x] != 0:
                        incs[y][x] += 1
                        final = False
    # return True if no more energy increases to apply for this step
    return final


def apply_step(grid):
    # The first energy increase is global and always applied
    incs = [[1] * len(grid[0]) for _ in range(len(grid))]
    force = True
    # Apply energy increments until no more flashes
    while True:
        final = apply_incs(grid, incs, force)
        force = False
        if final:
            break


def count_zeros(grid):
    return reduce(lambda res, r: res + r.count(0), grid, 0)


def solve_1(values, n_steps):
    grid = copy.deepcopy(values)  # destructive algo so make a copy of the input
    flash_count = 0
    for _ in range(n_steps):
        apply_step(grid)
        flash_count += count_zeros(grid)
    return flash_count


def solve_2(values):
    grid = copy.deepcopy(values)  # destructive algo so make a copy of the input
    step = 0
    while True:
        step += 1
        apply_step(grid)
        if count_zeros(grid) == len(grid) * len(grid[0]):  # could be embedded in apply_step or use early break
            return step


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values, 100))
    print("Part 2:", solve_2(input_values))

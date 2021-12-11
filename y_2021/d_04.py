from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    grids = []
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        drawings = [int(r) for r in f.readline().split(',')]
        rows = f.readlines()
    rows.append('')  # append a "terminator" empty string to ensure capturing the last grid
    grid = []
    for r in rows:
        r = r.strip()
        if not r:
            if len(grid) > 0:
                assert len(grid) == 5  # sanity
                grids.append(grid)
            grid = []
        else:
            grid.append([int(x) for x in r.split()])
    return (drawings, grids)


# turns a nxn matrix into 2*n sets of the rows & columns values
def grid_to_sets(grid):
    sets = []
    for r in grid:
        sets.append(set(r))
    for i in range(len(grid)):
        sets.append({r[i] for r in grid})
    return sets


def sum_unmarked(sgrid):
    unmarked = 0
    for s in sgrid:
        for e in s:
            unmarked += e
    # unmarked values are double counted in a sgrid
    return unmarked // 2


def solve_1(drawings, grids):
    sgrids = [grid_to_sets(grid) for grid in grids]
    res = None
    for d in drawings:
        for sgrid in sgrids:
            for s in sgrid:
                if d in s:
                    s.remove(d)
                    if len(s) == 0:
                        res = sgrid  # first winning grid found
            if res:
                break  # first winning grid found, skip the rest
        if res:
            break  # first winning grid found, stop drawing
    return sum_unmarked(res) * d


def solve_2(drawings, grids):
    sgrids = [grid_to_sets(grid) for grid in grids]
    res = None
    finished = set()
    for d in drawings:
        for i, sgrid in enumerate(sgrids):
            for s in sgrid:
                if d in s:
                    s.remove(d)
                    if len(s) == 0 and i not in finished:
                        finished.add(i)
                        if len(finished) == len(sgrids):
                            res = sgrids[i]  # last winning grid found
        if res:
            break  # stop drawing if target is found
    if not res:
        return None  # no solution
    return sum_unmarked(res) * d


if __name__ == "__main__":
    input_drawings, input_grids = parse_input()

    print("Part 1:", solve_1(input_drawings, input_grids))
    print("Part 2:", solve_2(input_drawings, input_grids))

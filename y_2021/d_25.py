from pathlib import Path
import time
import copy

VERBOSE = False


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for r in f.readlines():
            if r == "":
                continue
            res.append([v for v in r.strip()])
        return res


#####################################################################################################
# Solution 1: Use a grid, complexity ~ grid size
def print_landscape(lscape, display=None):
    if VERBOSE if display is None else display:
        print()
        for r in lscape:
            print("".join(r))
        print()


def iterate_landscape(lscape):
    moved = False
    w, h = len(lscape[0]), len(lscape)
    lscape_tmp = [["."] * w for _ in range(h)]
    for j in range(h):
        for i in range(w):
            if lscape[j][i] == ">":
                if lscape[j][(i + 1) % w] == ".":
                    lscape_tmp[j][(i + 1) % w] = ">"
                    moved = True
                else:
                    lscape_tmp[j][i] = ">"
            elif lscape[j][i] == "v":
                lscape_tmp[j][i] = "v"
    for j in range(h):
        for i in range(w):
            lscape[j][i] = lscape_tmp[j][i]
            lscape_tmp[j][i] = "."
    for i in range(w):
        for j in range(h):
            if lscape[j][i] == "v":
                if lscape[(j + 1) % h][i] == ".":
                    lscape_tmp[(j + 1) % h][i] = "v"
                    moved = True
                else:
                    lscape_tmp[j][i] = "v"
            elif lscape[j][i] == ">":
                lscape_tmp[j][i] = ">"
    for j in range(h):
        for i in range(w):
            lscape[j][i] = lscape_tmp[j][i]
    return moved


def solve_landscape(values):
    lscape = copy.deepcopy(values)
    count = 0
    print_landscape(lscape)
    while iterate_landscape(lscape):
        print_landscape(lscape)
        count += 1
    return count + 1


#####################################################################################################
# Solution 2: Use sets, complexist ~ population size
def lscape_to_lset(lscape):
    w, h = len(lscape[0]), len(lscape)
    r, d = set(), set()
    for j in range(h):
        for i in range(w):
            if lscape[j][i] == ">":
                r.add((i, j))
            elif lscape[j][i] == "v":
                d.add((i, j))
    return w, h, r, d


def landset_to_landscape(w, h, r, d):
    lscape = [["."] * w for _ in range(h)]
    for i, j in r:
        lscape[j][i] = ">"
    for i, j in d:
        lscape[j][i] = "v"
    return lscape


def print_landset(w, h, r, d):
    print_landscape(landset_to_landscape(w, h, r, d))


def iterate_landset(w, h, r, d):
    moved = False
    n = set()
    for i, j in r:
        p = ((i + 1) % w, j)
        if p not in r and p not in d and p not in n:
            n.add(p)
            moved = True
        else:
            n.add((i, j))
    r.clear()
    r.update(n)
    n = set()
    for i, j in d:
        p = (i, (j + 1) % h)
        if p not in r and p not in d and p not in n:
            n.add(p)
            moved = True
        else:
            n.add((i, j))
    d.clear()
    d.update(n)
    return moved


def solve_landset(values):
    w, h, r, d = lscape_to_lset(values)
    count = 0
    print_landset(w, h, r, d)
    while iterate_landset(w, h, r, d):
        print_landset(w, h, r, d)
        count += 1
    return count + 1


if __name__ == "__main__":
    input_values = parse_input()

    print_landscape(input_values, display=False)

    start_time = time.time()
    print(f"Part 1 (scape): {str(solve_landscape(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 1 (set)  : {str(solve_landset(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

from pathlib import Path
import re


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    dots = set()
    folds = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            m = re.search(r'(\d+),(\d+)', r.strip())
            if m:
                dots.add((int(m.group(1)), int(m.group(2))))
                continue
            m = re.search(r'fold along (.)=(\d+)', r.strip())
            if m:
                folds.append((m.group(1), int(m.group(2))))
    return dots, folds


def dot_matrix(dots):
    maxx, maxy = (max(d[i] for d in dots) for i in (0, 1))
    arr = [[False] * (maxx + 1) for _ in range(maxy + 1)]
    for x, y in dots:
        arr[y][x] = True
    return arr


def print_matrix(arr):
    print(' ' + ('-' * len(arr[0])) + ' ')
    for r in arr:
        print('|' + ''.join(('*' if v else ' ' for v in r)) + '|')
    print(' ' + ('-' * len(arr[0])) + ' ')
    print()


def fold(dots, direction, pos):
    # fold
    tdots = set()
    for x, y in dots:
        if (direction == 'x' and x == pos) or (direction == 'y' and y == pos):
            continue
        if direction == 'x' and x > pos:
            x = 2 * pos - x
        elif direction == 'y' and y > pos:
            y = 2 * pos - y
        tdots.add((x, y))
    # rebase
    minx, miny = (min({0} | {d[i] for d in tdots}) for i in (0, 1))
    rdots = set()
    for x, y in tdots:
        rdots.add((-minx + x, -miny + y))
    return rdots


def solve_1(dots, folds):
    return len(fold(dots, folds[0][0], folds[0][1]))


def solve_2(dots, folds):
    d = dots
    for f in folds:
        d = fold(d, f[0], f[1])
    return d


if __name__ == "__main__":
    input_dots, input_folds = parse_input()

    print("Part 1:", solve_1(input_dots, input_folds))
    print("Part 2:")
    print_matrix(dot_matrix(solve_2(input_dots, input_folds)))

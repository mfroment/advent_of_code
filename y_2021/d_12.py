from pathlib import Path
from collections import Counter


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = {}
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            a, b = r.strip().split('-')
            res.setdefault(a, set())
            res.setdefault(b, set())
            res[a].add(b)
            res[b].add(a)
        return res


def is_big(k):
    return k[0].upper() == k[0]


def complete_path_1(system, path):
    assert len(path) > 0
    # Check if path is complete and return if the case
    if path[-1] == 'end':
        return [path]
    visited = set(path)  # (doing that every call -> inefficient)
    # Complete the current WIP path
    completed_paths = []
    for n in system[path[-1]]:
        if is_big(n) or n not in visited:
            completed_paths.extend(complete_path_1(system, path + [n]))
    return completed_paths


def solve_1(values):
    return len(complete_path_1(values, ['start']))


def complete_path_2(system, path):
    assert len(path) > 0
    # Check if path is complete and return if the case
    if path[-1] == 'end':
        return [path]
    visited = Counter(path)  # (doing that every call -> inefficient)
    # Check if there is a small cave that was visited twice (doing that every call -> inefficient)
    has_two_small = False
    for k in visited:
        if not is_big(k) and visited[k] > 1:
            has_two_small = True
            break
    # Complete the current WIP path
    completed_paths = []
    for n in system[path[-1]]:
        if is_big(n) or n not in visited or (n != 'start' and not has_two_small):
            completed_paths.extend(complete_path_2(system, path + [n]))
    return completed_paths


def solve_2(values):
    return len(complete_path_2(values, ['start']))


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

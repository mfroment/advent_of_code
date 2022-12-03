import string
from pathlib import Path
import time


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([v for v in r.strip()])
        return res


ITEMS = string.ascii_lowercase + string.ascii_uppercase
PRIORITIES = {l: ITEMS.index(l) + 1 for l in ITEMS}


def common_item(*sets):
    candidates = set.intersection(*sets)
    assert (len(candidates) == 1)
    return candidates.pop()


def solve_1(values):
    total_priority = 0
    for v in values:
        c = common_item(set(v[:len(v) // 2]), set(v[len(v) // 2:]))
        total_priority += PRIORITIES[c]
    return total_priority


def solve_2(values):
    total_priority = 0
    for i in range(0, len(values) // 3):
        c = common_item(set(values[3 * i]), set(values[3 * i + 1]), set(values[3 * i + 2]))
        total_priority += PRIORITIES[c]
    return total_priority


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

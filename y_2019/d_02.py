from pathlib import Path
import time
import itertools


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append([int(v) for v in r.strip().split(',')])
        return res[0]


def process(ops, idx=0):
    if ops[idx] == 99:
        return True
    if ops[idx] not in {1, 2}:
        return False
    op, a, b, i = ops[idx:idx + 4]
    a, b = ops[a], ops[b]
    if ops[idx] == 1:
        ops[i] = a + b
    elif ops[idx] == 2:
        ops[i] = a * b
    idx = idx + 4
    return process(ops, idx)


def solve_1(values):
    vv = values[:]
    vv[1] = 12
    vv[2] = 2
    process(vv)
    return vv[0]


def solve_2(values):
    solved = False
    for a, b in itertools.product(range(100), range(100)):
        vv = values[:]
        vv[1], vv[2] = a, b
        success = process(vv)
        if success and vv[0] == 19690720:
            solved = True
            break
    if solved:
        return vv[1] * 100 + vv[2]
    else:
        return None


if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

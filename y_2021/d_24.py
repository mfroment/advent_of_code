import time
from collections import deque
from itertools import product
from pathlib import Path


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for r in f.readlines():
            tmp = tuple(intsafe(v) for v in r.strip().split(" "))
            res.append(tmp)
        return res


def intsafe(s):
    try:
        return int(s)
    except:
        return s


def get(vars, val):
    if isinstance(val, int):
        return val
    else:
        return vars[val]


def process(seq, inps):
    vars = {"w": 0, "x": 0, "y": 0, "z": 0}
    for s in seq:
        if s[0] == "inp":
            vars[s[1]] = intsafe(inps.popleft())
        else:
            inst, a, b = s
            vb = get(vars, b)
            if inst == "add":
                vars[a] += vb
            elif inst == "mul":
                vars[a] *= vb
            elif inst == "div":
                vars[a] = div(vars[a], vb)
            elif inst == "mod":
                vars[a] = vars[a] % vb
            elif inst == "eql":
                vars[a] = 1 if (vars[a] == vb) else 0
            else:
                assert False
        print(s, vars, inps)
    return vars["z"] == 0


def process(seq, inps):
    vars = {"w": 0, "x": 0, "y": 0, "z": 0}
    for s in seq:
        if s[0] == "inp":
            vars[s[1]] = intsafe(inps.popleft())
        else:
            inst, a, b = s
            vb = get(vars, b)
            if inst == "add":
                vars[a] += vb
            elif inst == "mul":
                vars[a] *= vb
            elif inst == "div":
                vars[a] = div(vars[a], vb)
            elif inst == "mod":
                vars[a] = vars[a] % vb
            elif inst == "eql":
                vars[a] = 1 if (vars[a] == vb) else 0
            else:
                assert False
        print(s, vars, inps)
    return vars["z"] == 0


def div(x, y):
    t = abs(x) // abs(y)
    return t if x * y > 0 else -t


def len_seq(seq):
    return sum(1 if s[0] == "inp" else 0 for s in seq)


def solve_1(values):
    res = ""
    worlds = product(*(range(9, 0, -1) for _ in range(len_seq(values))))

    for w in worlds:
        inps = deque(w)
        print(w)
        if process(values, inps):
            break
    return int(res)


def solve_2(values):
    return None


if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)
    print(len_seq(input_values))

    start_time = time.time()
    print(f"Part 1: {solve_1(input_values):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    # start_time = time.time()
    # print(f"Part 2: {solve_2(input_values):<30}{'(':>30}{time.time() - start_time:.3f}s)")

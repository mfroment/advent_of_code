from pathlib import Path
from math import isqrt

GENERATOR = 7
MODULUS = 20201227


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        return [int(r) for r in f.readlines() if r != '']


def modular_log(a, b, n):
    m = isqrt(n) + 1
    comps = dict()
    c = 1
    for j in range(m):
        comps[c] = j
        c = c * a % n
    ainv = pow(a, -m, n)
    g = b
    for i in range(m):
        if g in comps:
            return i * m + comps[g]
        g = (g * ainv) % n
    return None


def solve_1(pkeys):
    l0 = modular_log(GENERATOR, pkeys[0], MODULUS)
    return pow(pkeys[1], l0, MODULUS)


def solve_2(s):
    return None


if __name__ == "__main__":
    input_pkeys = parse_input()

    print("Part 1:", solve_1(input_pkeys))
    print("Part 2:", solve_1(input_pkeys))

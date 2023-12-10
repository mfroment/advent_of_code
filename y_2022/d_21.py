import time
import re
from copy import deepcopy
from statistics import mean
import sympy as sy
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = dict()
    for section in sections:
        for line in section:
            tokens = re.split(r"\s+", line, maxsplit=0)
            res[tokens[0][:-1]] = [aocu.s2i(t) for t in tokens[1:]]
            if len(res[tokens[0][:-1]]) == 1:
                res[tokens[0][:-1]] = res[tokens[0][:-1]][0]
    return res


def get_num(key, numbers, ops):
    if key in numbers:
        pass
    elif isinstance(ops[key], int):
        numbers[key] = ops[key]
    else:
        a, op, b = ops[key]
        va = get_num(a, numbers, ops)
        vb = get_num(b, numbers, ops)
        numbers[key] = eval(str(va) + op + str(vb))
    return numbers[key]


def solve_1(ops):
    numbers = dict()
    return int(get_num('root', numbers, ops))


def solve_2_search(ops):
    # Leap of faith: Newton-Raphson will work (hinted by observation of linearity...)
    MAX_TRIES = 10
    SEARCH_RANGE = 10

    ops = deepcopy(ops)
    k1, _, k2 = ops['root']
    ops['root'] = [k1, '-', k2]

    def find_root(x):
        f = dict()
        for xx in range(x - SEARCH_RANGE, x + SEARCH_RANGE + 1):
            f[xx] = compute_f(xx)
            if f[xx] == 0:
                return xx, True
        df = dict()
        for xx in range(x - SEARCH_RANGE + 1, x + SEARCH_RANGE + 1):
            df[xx] = f[xx] - f[xx - 1]
        delta_f = mean(df.values())
        return int(x - f[x] / delta_f), False

    def compute_f(x):
        ops['humn'] = x
        numbers = dict()
        return get_num('root', numbers, ops)

    x = 0
    for _ in range(MAX_TRIES):
        x, is_root = find_root(x)
        if is_root:
            return x
    return None


def get_expr(key, exprs, ops):
    if key in exprs:
        pass
    elif isinstance(ops[key], int):
        exprs[key] = sy.parse_expr(str(ops[key]))
    elif len(ops[key]) == 1:
        a, = ops[key]
        exprs[key] = sy.parse_expr(a)
    else:
        a, op, b = ops[key]
        va = get_expr(a, exprs, ops)
        vb = get_expr(b, exprs, ops)
        exprs[key] = sy.parse_expr("(" + str(va) + ")" + op + "(" + str(vb) + ")")
    return exprs[key]


def solve_2_symbolic(ops):
    ops = deepcopy(ops)
    k1, _, k2 = ops['root']
    ops['root'] = [k1, '-', k2]
    ops['humn'] = ['humn']
    exprs = dict()
    return sy.solve(get_expr('root', exprs, ops), sy.Symbol('humn'))[0]


solve_2 = solve_2_symbolic


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1           : {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2 (search)  : {str(solve_2_search(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    print(f"Part 2 (symbolic): {str(solve_2_symbolic(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

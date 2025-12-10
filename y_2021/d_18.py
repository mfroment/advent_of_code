from pathlib import Path
import ast


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for r in f.readlines():
            if r == "":
                continue
            res.append(ast.literal_eval(r.strip()))
        return res


def c2i(c):
    try:
        return int(c)
    except:
        return c


def l2s(lst):
    return [c2i(x) for x in str(lst) if x not in {" ", ","}]


def s2l(s):
    ns = []
    for i, x in enumerate(s):
        ns.append(x)
        if i < len(s) - 1:
            if (x == "]" or isinstance(x, int)) and s[i + 1] != "]":
                ns.append(",")
    return ast.literal_eval("".join([str(x) for x in ns]))


def explode(s):
    last_int = None
    d = 0
    for i, x in enumerate(s):
        if x == "[":
            d += 1
        elif x == "]":
            d -= 1
        else:  # integer
            if d > 4 and isinstance(s[i + 1], int):
                ls = s[: i - 1]
                rs = s[i + 3 :]
                if last_int is not None:  # update left int if any
                    ls[last_int] += x
                for j, y in enumerate(rs):  # find right int if any and update it
                    if isinstance(y, int):
                        rs[j] += s[i + 1]
                        break
                return True, ls + [0] + rs
            last_int = i
    return False, s


def split(s):
    for i, x in enumerate(s):
        if isinstance(x, int) and x >= 10:
            return True, s[:i] + ["[", x // 2, (x + 1) // 2, "]"] + s[i + 1 :]
    return False, s


def process(s):
    while True:
        es, s = explode(s)
        if es:
            continue
        ps, s = split(s)
        if ps:
            continue
        break
    return s


def magnitude(x):
    if isinstance(x, int):
        return x
    a, b = x
    return 3 * magnitude(a) + 2 * magnitude(b)


def solve_1(values):
    res = None
    for v in values:
        if res is not None:
            res = [res, v]
        else:
            res = v
        res = s2l(process(l2s(res)))
    return magnitude(res)


def solve_2(values):
    res = 0
    for i, v in enumerate(values):
        for j, w in enumerate(values):
            if i != j:
                res = max(res, magnitude(s2l(process(l2s([v, w])))))
    return res


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

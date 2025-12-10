from pathlib import Path
import re


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        r = " " + f.readline().strip() + " "  # pad template with terminators
        polypairs = dict()
        for i in range(len(r) - 1):
            polypairs[r[i : i + 2]] = polypairs.get(r[i : i + 2], 0) + 1

        insertions = dict()
        for r in f.readlines():
            if r.strip() == "":
                continue
            m = re.search(r"(..) -> (.)", r.strip())
            insertions[m.group(1)] = m.group(2)
        return polypairs, insertions


def p_insert(polypairs, insertions):
    npps = dict()
    for p in polypairs:
        if p in insertions:
            for np in (p[0] + insertions[p], insertions[p] + p[1]):
                npps[np] = npps.get(np, 0) + polypairs[p]
        else:
            npps[p] = npps.get(p, 0) + polypairs[p]
    return npps


def breakup(polypairs):
    # from polymer pair count to elment count (excluding ' ' terminators)
    res = dict()
    for p, v in polypairs.items():
        for c in list(p):
            if c != " ":  # do not include terminators
                res[c] = res.get(c, 0) + v
    return res


def solve(polypairs, insertions, n_iter):
    pps = polypairs
    for _ in range(n_iter):
        pps = p_insert(pps, insertions)
    pes = breakup(pps)
    return max(pes.values()) // 2 - min(pes.values()) // 2


def solve_1(polypairs, insertions):
    return solve(polypairs, insertions, 10)


def solve_2(polypairs, insertions):
    return solve(polypairs, insertions, 40)


if __name__ == "__main__":
    input_polypairs, input_insertions = parse_input()

    print("Part 1:", solve_1(input_polypairs, input_insertions))
    print("Part 2:", solve_2(input_polypairs, input_insertions))

import time
import re
import aoc.utils as aocu
from functools import cache


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            spring, breakage = line.split(" ")
            breakage = tuple([int(b) for b in breakage.split(",")])
            sub_res.append((spring, breakage))
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


# This is the brute force solution I came up with that was compatible
# with my workday, but not with the scale of the problem for part 2 😅
def naive_solve(values):
    def expand_spring(spring, prev=[""]):
        if len(spring) == 0:
            return prev
        if spring[0] == "?":
            return expand_spring(spring[1:], [p + "." for p in prev] + [p + "#" for p in prev])
        else:
            return expand_spring(spring[1:], [p + spring[0] for p in prev])

    def breakage_to_pattern(breakage):
        pattern = r"^\.*" + "".join([r"#{" + str(b) + r"}\.+" for b in breakage])
        pattern = pattern[:-1] + r"*$"
        return pattern

    res = 0
    for spring, breakage in values:
        all_spring = expand_spring(spring)
        breakage_pattern = breakage_to_pattern(breakage)
        for s in all_spring:
            if re.search(breakage_pattern, s):
                res += 1
    return res


# This is the solution I came up with after work, efficient enough for part 2
# (EDIT: slightly modified from the original version, to use the cache decorator instead of a dict for memoization)
@cache
def count_spring_breakages(spring, breakage):
    spring = spring.strip(".")

    if len(breakage) == 0:
        if re.match(r"^[.?]*$", spring):
            return 1
        else:
            return 0
    if len(spring) == 0:
        return 0

    if spring[0] == "?":
        nb = count_spring_breakages(spring[1:], breakage) + count_spring_breakages("#" + spring[1:], breakage)
        return nb

    assert spring[0] == "#"  # because we stripped "." / checked for leading "?"
    b, bs = breakage[0], tuple(breakage[1:])
    if re.match(r"^#[#?]{" + str(b - 1) + r"}(\.|\?|$)", spring):
        ns = spring[(b + 1) :]
        nb = count_spring_breakages(ns, bs)
        return nb
    else:
        return 0


def solve(values):
    res = 0
    for spring, breakage in values:
        res += count_spring_breakages(spring, breakage)
    return res


def solve_1(values):
    return solve(values)


def solve_2(values):
    exp_values = [("?".join([spring] * 5), tuple(breakage * 5)) for spring, breakage in values]
    return solve(exp_values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{----time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

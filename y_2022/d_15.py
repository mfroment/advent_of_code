import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.search(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$",
                               line).groups()
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def covered_hrange(sx, sy, bx, by, ty):
    d = abs(sx - bx) + abs(sy - by)
    if 0 <= abs(sy - ty) <= d:
        dd = d - abs(sy - ty)
        return [sx - dd, sx + dd]
    return []


def range_to_set(rng):
    if len(rng) == 0:
        return set()
    else:
        return set(range(rng[0], rng[1] + 1))


def union_many_intervals(intervals):
    if len(intervals) == 0 or len(intervals) == 1:
        return intervals
    intervals = sorted([interval for interval in intervals if len(interval) > 0])
    intervals.sort(key=lambda x: x[0])
    res = [intervals[0]]
    for interval in intervals[1:]:
        if interval[0] <= res[-1][1]:
            res[-1][1] = max(res[-1][1], interval[1])
        else:
            res.append(interval)
    return res


def intersect_one_interval_to_many_intervals(one, intervals):
    assert (len(one) == 2)
    # assume the intervals have been union'ed
    res = []
    for interval in intervals:
        a, b = max(one[0], interval[0]), min(one[1], interval[1])
        if a <= b:
            res.append([a, b])
    return res


def solve_1_naive(values, ty):
    excluded = set()
    for sx, sy, bx, by in values:
        excluded |= range_to_set(covered_hrange(sx, sy, bx, by, ty))
    for _, _, bx, by in values:
        if by == ty and bx in excluded:
            excluded.remove(bx)
    return len(excluded)


def solve_1_faster(values, ty):
    covered = []
    beacons = set()
    for sx, sy, bx, by in values:
        covered.append(covered_hrange(sx, sy, bx, by, ty))
        # mark possible beacons on the boundary of a given interval, not to be counted
        if by == ty:
            beacons.add(bx)
    merged_covered = union_many_intervals(covered)
    excluded_count = -len(beacons)
    for interval in merged_covered:
        excluded_count += interval[1] - interval[0] + 1
    return excluded_count


solve_1 = lambda values: solve_1_faster(values, 2000000)


def solve_2_slow(values, tsx, tex, tsy, tey):
    for tty in range(tsy, tey + 1):
        covered = []
        for sx, sy, bx, by in values:
            covered.append(covered_hrange(sx, sy, bx, by, tty))
        merged_covered = union_many_intervals(covered)
        inter = intersect_one_interval_to_many_intervals([tsx, tex], merged_covered)
        if len(inter) != 1:
            ttx = inter[0][1] + 1
            return 4000000 * ttx + tty
    return None

solve_2 = lambda values: solve_2_slow(values, 0, 4000000, 0, 4000000)

if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

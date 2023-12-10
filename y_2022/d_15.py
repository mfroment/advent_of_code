import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
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


def md(x, y, xx, yy):
    return abs(x - xx) + abs(y - yy)


def covered_hrange(sx, sy, bx, by, ty):
    d = md(sx, sy, bx, by)
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


# Bad space complexity
def solve_1_set(values, ty):
    excluded = set()
    for sx, sy, bx, by in values:
        excluded |= range_to_set(covered_hrange(sx, sy, bx, by, ty))
    for _, _, bx, by in values:
        if by == ty and bx in excluded:
            excluded.remove(bx)
    return len(excluded)


def solve_1_interval_merge(values, ty):
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


solve_1 = lambda values: solve_1_interval_merge(values, 2000000)


# Bad time complexity
def solve_2_interval_merge(values, tsx, tex, tsy, tey):
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


def solve_2_losange_boundaries(values, tsx, tex, tsy, tey):
    # Since there is only 1 solution, it must lie at the intersection of
    # 2 lines that are defined by the 1-width gap existing between 2
    # sensor "exclusion losanges".
    # First we find all such lines (resp. slash lines = / , backslash
    # lines = \ ; marked by the value of x at their intersection with y = 0),
    # Then the intersections of all slashlines with all backslash lines.
    # Then the intersections that exist in the provided target area.
    # Then the intersections that are outside all sensors' exclusion areas.
    # (there should be exactly one)

    # For each beacon, record the x value at y=0 of the leftmost and
    # rightmost slash & backlash lines (pen & paper & simple maths):
    beacon_slash_lines = []
    beacon_backslash_lines = []
    for sx, sy, bx, by in values:
        d = md(sx, sy, bx, by)
        beacon_slash_lines.append([sx + sy - d - 1, sx + sy + d + 1])
        beacon_backslash_lines.append([sx - sy - d - 1, sx - sy + d + 1])
    # Now for each pair of sensors, if the leftmost slashline of one sensor
    # matches the rightmost slashline of the other sensor, keep it (check both cases).
    # Ex:   \ <--- a candidate backslash line
    #      /\\ /\
    #     /  \\\/
    #     \  /\\
    #      \/  \\
    # Then do the same for backslash lines.
    slash_lines, backslash_lines = set(), set()
    for beacon_slanted_lines, slanted_lines in (
            (beacon_slash_lines, slash_lines),
            (beacon_backslash_lines, backslash_lines)
    ):
        for i, (x1, x2) in enumerate(beacon_slanted_lines):
            for xx1, xx2 in beacon_slanted_lines[i + 1:]:
                if x1 == xx2:
                    slanted_lines.add(x1)
                if x2 == xx1:
                    slanted_lines.add(x2)
    # Compute all intersections:
    intersections = set()
    for sl_x in slash_lines:
        for bsl_x in backslash_lines:
            # integer lines where x's parity is different do not intersect
            if (sl_x + bsl_x) % 2 == 0:
                intersections.add(((sl_x + bsl_x) // 2, (sl_x - bsl_x) // 2))
    # Only keep intersections not in the target area
    intersections = {(x, y) for (x, y) in intersections if tsx <= x <= tex and tsy <= y <= tey}
    # Only keep intersections not in any sensor's exclusion losange
    # (there should be one and only one)
    intersections = {(x, y) for (x, y) in intersections if
                     all(md(sx, sy, x, y) > md(sx, sy, bx, by) for sx, sy, bx, by in values)}
    assert (len(intersections) == 1)
    (x, y) = intersections.pop()
    return 4000000 * x + y


solve_2 = lambda values: solve_2_losange_boundaries(values, 0, 4000000, 0, 4000000)

if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

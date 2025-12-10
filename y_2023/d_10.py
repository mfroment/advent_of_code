import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    return aocu.read_input(file, suffix)[0]


def get_graph(res):
    CONNECTIONS = {
        "|": {(0, -1), (0, 1)},
        "-": {(-1, 0), (1, 0)},
        "L": {(0, -1), (1, 0)},
        "J": {(0, -1), (-1, 0)},
        "7": {(0, 1), (-1, 0)},
        "F": {(0, 1), (1, 0)},
        ".": set(),
        "S": set(),
    }
    g = {}
    start = None
    for j, line in enumerate(res):
        for i, c in enumerate(line):
            if c == "S":
                start = (i, j)
            g[(i, j)] = {(i + dx, j + dy) for dx, dy in CONNECTIONS[c]}
    for k, v in g.items():
        if start in v:
            g[start].add(k)
    return g, start


def get_loop(g, start):
    s = start
    loop = []  # for the ability to move forward in the loop
    loops = set()  # for fast membership testing
    while True:
        loop.append(s)
        loops.add(s)
        a, b = g[s]
        if a not in loops:
            s = a
        elif b not in loops:
            s = b
        else:
            break
    return loop


def solve_1(values):
    g, start = get_graph(values)
    loop = get_loop(g, start)
    return len(loop) // 2


def solve_2(values):
    # Approach:
    # Traverse the loop (in the arbitrary direction we used to populate it), marking the "left/right" side
    # of the loop as we go forward.
    # Then we can determine which side of the loop the remaining tiles are by doing a flood fill of the grid,
    # starting from the tiles immediately outside the loop, for which the side is now known.
    # Finally we figure out which side, left or right, is the outer side, then conversely we get the inner side
    # and can count the inner tiles.

    # Add one row at the end of the grid so we can figure which side is outer/inner
    # This row will belong to the outer side.
    w, h = len(values[0]), len(values) + 1
    values.append(["."] * w)

    g, start = get_graph(values)
    loop = get_loop(g, start)
    sloop = set(loop)  # for fast membership testing

    fillables = set()
    grid_sides = {(x, y): None for x in range(w) for y in range(h)}
    pps, ps = loop[-2], loop[-1]
    for s in loop:
        grid_sides[ps] = "loop"
        pdx, pdy = ps[0] - pps[0], ps[1] - pps[1]
        dx, dy = s[0] - ps[0], s[1] - ps[1]
        # determine if we're moving forward, turning left or turning right
        if (dx, dy) == (
            pdx,
            pdy,
        ):  # moving forward, 1 point to the left, 1 point to the right
            lpos = {(ps[0] - pdy, ps[1] + pdx)}
            rpos = {(ps[0] + pdy, ps[1] - pdx)}
        elif (dx, dy) == (-pdy, pdx):  # turning left, 2 points to the right
            lpos = set()
            rpos = {(ps[0] + pdx, ps[1] + pdy), (ps[0] + pdy, ps[1] - pdx)}
        elif (dx, dy) == (pdy, -pdx):  # turning right, 2 points to the left
            lpos = {(ps[0] + pdx, ps[1] + pdy), (ps[0] - pdy, ps[1] + pdx)}
            rpos = {}
        else:  # backtracking, shouldn't happen
            assert False

        # exclude points that are outside the grid or inside the loop
        for pos in lpos:
            if pos not in sloop and 0 <= pos[0] < w and 0 <= pos[1] < h:
                grid_sides[pos] = "left"
                fillables.add(pos)
        for pos in rpos:
            if pos not in sloop and 0 <= pos[0] < w and 0 <= pos[1] < h:
                grid_sides[pos] = "right"
                fillables.add(pos)

        pps, ps = ps, s

    # flood fill the grid
    while fillables:
        s = fillables.pop()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            candidate = (s[0] + dx, s[1] + dy)
            # only retain points that are inside the grid and not already filled
            if 0 <= candidate[0] < w and 0 <= candidate[1] < h and grid_sides[candidate] is None:
                grid_sides[candidate] = grid_sides[s]
                fillables.add(candidate)

    # thanks to appending a row of '.'s, we know that it belongs to the outer side, so we can figure the inner side
    inner_side = "left" if grid_sides[(0, h - 1)] == "right" else "right"

    return sum(1 for v in grid_sides.values() if v == inner_side)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

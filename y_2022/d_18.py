import time
import re
from collections import deque
from itertools import product

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = set()
    for line in sections[0]:
        tokens = re.split(r",", line, maxsplit=0)
        tokens = tuple(aocu.s2i(t) for t in tokens)
        res.add(tokens)
    return res


def get_neighbours(c):
    x, y, z = c
    return {
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    }


def get_surface(c, cublets):
    return sum(nb not in cublets for nb in get_neighbours(c))


def solve_1(cublets):
    return sum(get_surface(c, cublets) for c in cublets)


def solve_2(cublets):
    # Compute a "cast" over the lava droplets, via BFS, use it, and compute the surface of the solid object.

    # First compute an enclosure that contains the cublets, with a 1 cube-width margin
    xl = min(x for (x, y, z) in cublets) - 1
    xu = max(x for (x, y, z) in cublets) + 1
    yl = min(y for (x, y, z) in cublets) - 1
    yu = max(y for (x, y, z) in cublets) + 1
    zl = min(z for (x, y, z) in cublets) - 1
    zu = max(z for (x, y, z) in cublets) + 1
    enclosure = {(x, y, z) for x, y, z in product(range(xl, xu + 1), range(yl, yu + 1), range(zl, zu + 1))}

    # Starting from the "origin" of the enclosure, find cubes in the enclosure that form
    # a cast over the cublets. Do a BFS start from a corner of the enclosure.
    # The "seen" cublets form the cast.
    start_cublet = (xl, yl, zl)
    seen = set()
    queue = deque()
    queue.append(start_cublet)
    seen.add(start_cublet)
    while queue:
        parent = queue.popleft()
        for child in get_neighbours(parent):
            if child in enclosure and child not in seen and child not in cublets:
                queue.append(child)
                seen.add(child)
    # Now cast the solid item (= closed space occupied by the cublets, without the air bubbles)
    # and compute its surface
    solid = enclosure - seen
    return sum(get_surface(c, solid) for c in solid)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

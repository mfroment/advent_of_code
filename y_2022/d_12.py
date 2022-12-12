# Used Dijsktra, starting from destination and backtracking to start -> this helps for part 2
# Also, Dijsktra, without a proper priority queue -> well...
# Also, Dijsktra, when BFS is good enough -> facepalm

import time
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            sub_res.append(line)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def height_difference(p, q):
    return ord(q) - ord(p)


def graphify(values):
    S, E = None, None
    pos = dict()
    ly = len(values)
    lx = len(values[0])
    for y, row in enumerate(values):
        for x, v in enumerate(row):
            if v == 'S':
                S = (x, y)
                v = 'a'
            if v == 'E':
                E = (x, y)
                v = 'z'
            pos[(x, y)] = {'v': v}
    for y, row in enumerate(values):
        for x, v in enumerate(row):
            neighbours = set()
            for xx, yy in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                # Note: edge direction is flipped, (accessible) destination node -> origin node
                #   This helps with Part 2 as we want to find shortest paths from all 'a's to E
                if 0 <= xx < lx and 0 <= yy < ly and height_difference(pos[(x, y)]['v'], pos[(xx, yy)]['v']) >= -1:
                    neighbours.add((xx, yy))
            pos[(x, y)]['n'] = neighbours
    return pos, S, E


def dijkstra(pos, S):
    unvisited = set(pos.keys())
    distances = dict()
    distances[S] = 0
    # pred = {}
    # pred[S] = None
    pending = {S}  # Not a proper priority queue, O(n) removals due to min over the whole set.
    while len(pending) > 0:
        p = min(pending, key=lambda p: distances[p])
        pending.remove(p)
        unvisited.remove(p)
        for n in pos[p]['n']:
            if n in unvisited:
                pending.add(n)
                if n not in distances or distances[n] > distances[p] + 1:
                    distances[n] = distances[p] + 1
                    # pred[n] = p
    return distances


def solve_1(values):
    pos, S, E = graphify(values)
    return dijkstra(pos, E)[S]


def solve_2(values):
    pos, _, E = graphify(values)
    distances = dijkstra(pos, E)
    return min(distances[p] for p in distances.keys() if pos[p]['v'] == 'a')


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

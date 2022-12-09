import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            # tokens = re.search(r"^(.+)-(.+)-(.+)-(.+)$", r).groups()
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def pos_diff(p, q):
    px, py = p
    qx, qy = q
    res = (qx - px, qy - py)
    return res


def pos_add(p, q):
    px, py = p
    qx, qy = q
    res = (qx + px, qy + py)
    return res


def solve_for_length(values, rope_length):
    rope = [(0, 0) for _ in range(0, rope_length)]
    visited = {(0, 0)}
    for d, m in values:
        dd = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}[d]
        for mm in range(0, m):
            rope[0] = pos_add(rope[0], dd)
            for i in range(1, len(rope)):
                dx, dy = pos_diff(rope[i], rope[i - 1])
                move = False
                if dx > 1:
                    dx = 1
                    move = True
                elif dx < -1:
                    dx = -1
                    move = True
                if dy > 1:
                    dy = 1
                    move = True
                elif dy < -1:
                    dy = -1
                    move = True
                if move:
                    rope[i] = pos_add(rope[i], (dx, dy))
            visited.add(rope[-1])
    return len(visited)


def solve_1(values):
    return solve_for_length(values, 2)


def solve_2(values):
    return solve_for_length(values, 10)


if __name__ == "__main__":
    input_values = parse_input()

    print(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

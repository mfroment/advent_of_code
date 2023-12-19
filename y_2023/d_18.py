import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            a, b, c = re.split(r",|-|\s+", line, maxsplit=0)
            tokens = [a, int(b), c[2:-1]]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def get_vertices(instructions):
    vertices = [(0, 0)]
    for i, d in instructions:
        vertices.append((vertices[-1][0] + i * d[0], vertices[-1][1] + i * d[1]))
    return vertices


def compute_capacity(vertices):
    area = 0
    for i in range(1, len(vertices)):
        area += (vertices[i][1] + vertices[i-1][1]) * (vertices[i-1][0] - vertices[i][0])
    area = abs(area) // 2
    perimeter = 0
    for i in range(1, len(vertices)):
        perimeter += abs(vertices[i][0] - vertices[i-1][0]) + abs(vertices[i][1] - vertices[i-1][1])
    return area + perimeter // 2 + 1


def solve_1(values):
    DIRS = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }
    instructions = [(int(v[1]), DIRS[v[0]]) for v in values]
    vertices = get_vertices(instructions)
    return compute_capacity(vertices)


def solve_2(values):
    DIRS = {
        '0': (1, 0),
        '1': (0, 1),
        '2': (-1, 0),
        '3': (0, -1)
    }
    instructions = [(int(v[2][:-1], 16), DIRS[v[2][-1]]) for v in values]
    vertices = get_vertices(instructions)
    return compute_capacity(vertices)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

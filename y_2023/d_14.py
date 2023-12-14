import time
import aoc.utils as aocu
from collections import Counter


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    return aocu.reduce_input(sections)  # dimensionality reduction

# I'd rather rotate the grid than code the 4 cases of sliding rocks...

def rotate_clockwise(matrix, times):
    # 2 out of 4 cases aren't needed, but I might need them in a future problem...
    if times % 4 == 0:
        return matrix
    if times % 4 == 1:
        r = zip(*reversed(matrix))
    if times % 4 == 2:
        r = reversed([reversed(line) for line in matrix])
    if times % 4 == 3:
        r = reversed(list((zip(*matrix))))
    return [ "".join(line) for line in r ]


def slide_left_line(line):
    elems = line.split("#")
    nelems = []
    for e in elems:
        c = Counter(e)
        nelems.append("O" * c["O"] + "." * c["."])
    return "#".join(nelems)


def slide_left(matrix):
    return [ slide_left_line(line) for line in matrix ]


def compute_load(matrix):
    res = 0
    for i, line in enumerate(reversed(matrix)):
        c = Counter(line)
        res += c["O"] * (i+1)
    return res


def solve_1(values):
    rv = rotate_clockwise(values, -1)
    rv = slide_left(rv)
    rv = rotate_clockwise(rv, 1)
    return compute_load(rv)


def perform_one_cycle(values):
    rv = rotate_clockwise(values, -1)
    for _ in range(4):
        rv = slide_left(rv)
        rv = rotate_clockwise(rv, 1)    
    return rotate_clockwise(rv, 1)


def solve_2(values):
    N = 1000000000
    seen = dict()
    i = 0
    while i < N:
        k = "-".join(values)
        if k in seen:
            s = seen[k]
            l = i - s
            i = s + ((N - s) // l) * l
            if i == N:  # edge case, unlikely to happen
                break
        else:
            seen[k] = i
        values = perform_one_cycle(values)
        i+=1
    return compute_load(values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

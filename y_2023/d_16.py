import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            sub_res.append(list(line))
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def compute_energy(grid, start_beam = ((0, 0), (1, 0))):
    w = len(grid[0])
    h = len(grid)
    energies = [ [ 0 for _ in range(w) ] for _ in range(h) ]
    seen_beams = set()
    beams = { start_beam }
    while beams:
        (i, j), (di, dj) = beams.pop()
        seen_beams.add(((i, j), (di, dj)))
        energies[j][i] = 1
        deltas = set()
        if grid[j][i] == '\\':
            deltas.add((dj, di))
        elif grid[j][i] == '/':
            deltas.add((-dj, -di))
        elif grid[j][i] == '|':
            if di == 0:
                deltas.add((di,dj))
            else:
                deltas |= { (0,-1), (0,1) }
        elif grid[j][i] == '-':
            if dj == 0:
                deltas.add((di,dj))
            else:
                deltas |= { (-1,0), (1,0) }
        elif grid[j][i] == '.':
            deltas.add((di,dj))
        else:
            # unreachable
            assert False
        for ndi, ndj in deltas:
            ni, nj = i+ndi, j+ndj
            nbeam = ((i+ndi, j+ndj), (ndi, ndj))
            if 0 <= ni < w and 0 <= nj < h and nbeam not in seen_beams:
                beams.add(nbeam)
    return sum(sum(r) for r in energies)


def solve_1(values):
    return compute_energy(values)


def solve_2(values):
    max_energy = 0
    w = len(values[0])
    h = len(values)
    for j in range(len(values)):
        max_energy = max(max_energy, compute_energy(values, ((0, j), (1, 0))))
        max_energy = max(max_energy, compute_energy(values, ((w-1, j), (-1, 0))))
    for i in range(len(values[0])):
        max_energy = max(max_energy, compute_energy(values, ((i, 0), (0, 1))))
        max_energy = max(max_energy, compute_energy(values, ((i, h-1), (0, -1))))
    return max_energy


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

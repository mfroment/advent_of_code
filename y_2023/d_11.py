import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [1 if t == "." else "#" for t in line]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def get_expanded_universe(universe, expansion_factor):
    res = [line[:] for line in universe]
    for line in res:
        if not any(t == "#" for t in line):
            for i in range(len(line)):
                line[i] = expansion_factor
    for i in range(len(res[0])):
        if not any(t == "#" for t in [line[i] for line in res]):
            for line in res:
                line[i] = expansion_factor
    return res


def get_galaxies(universe):
    galaxies = set()
    vshift = 0
    for line in universe:
        hshift = 0
        for c in line:
            if c == "#":
                galaxies.add((hshift, vshift))
            hshift += 1 if c == "#" else c
        vshift += 1 if line[0] == "#" else line[0]
    return galaxies


def solve(universe, expansion_factor):
    expanded_universe = get_expanded_universe(universe, expansion_factor)
    galaxies = get_galaxies(expanded_universe)
    d = 0
    while len(galaxies) > 1:
        current_galaxy = galaxies.pop()
        for other_galaxy in galaxies:
            d += abs(current_galaxy[0] - other_galaxy[0]) + abs(current_galaxy[1] - other_galaxy[1])
    return d


def solve_1(values):
    return solve(values, 2)


def solve_2(values):
    return solve(values, 1000000)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

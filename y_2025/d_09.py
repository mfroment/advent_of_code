import re
import time

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    res = 0
    for i, v in enumerate(values):
        for w in values[i+1:]:
            vx, vy = v
            wx, wy = w
            res = max(res, (abs(vx-wx)+1) * (abs(vy-wy)+1))
    return res


def solve_2(values):
    # Create a compacted representation of the floor, mapping unique xs and ys

    # Unique xs and ys, padded with strict outer bounds (= "outside")
    oxs = sorted(set(v[0] for v in values))
    oys = sorted(set(v[1] for v in values))
    oxs = [min(oxs)-1] + oxs + [max(oxs)+1]
    oys = [min(oys)-1] + oys + [max(oys)+1]
    # Coordinates remapped on the compacted representation
    compacted_coordinates = [ [oxs.index(v[0]), oys.index(v[1])] for v in values ]
    # Floor in the compacted coordinates
    compacted_grid = [[None for _ in range(len(oxs))] for __ in range(len(oys))]
    
    # 1. Mark the red tiles red
    for cvx, cvy in compacted_coordinates:
        compacted_grid[cvy][cvx]='R'

    # 2. Mark the green tile green
    compacted_coordinates_shifted = compacted_coordinates[1:] + [compacted_coordinates[0]]
    for i, (cvx, cvy) in enumerate(compacted_coordinates):
        cwx, cwy = compacted_coordinates_shifted[i]
        assert cvx == cwx or cvy == cwy
        if cvx == cwx:
            for cny in range(min(cvy,cwy)+1,max(cvy,cwy)):
                assert compacted_grid[cny][cvx] is None
                compacted_grid[cny][cvx] = 'G'
        if cvy == cwy:
            for cnx in range(min(cvx,cwx)+1,max(cvx,cwx)):
                assert compacted_grid[cvy][cnx] is None
                compacted_grid[cvy][cnx] = 'G'

    # 3. Mark the outside tiles outside (flood fill)
    outside = {(0,0)}
    while outside:
        cvx,cvy = outside.pop()
        compacted_grid[cvy][cvx]='O'
        for cnx, cny in (cvx-1,cvy), (cvx+1,cvy), (cvx,cvy-1), (cvx, cvy+1):
            if cnx < 0 or cnx >= len(compacted_grid[0]) or cny < 0 or cny >= len(compacted_grid):
                continue
            if compacted_grid[cny][cnx] is not None:
                continue
            outside.add((cnx, cny)) 

    # Find size of largest rectangle with red tiles at the opposite corner, containing no outside tile
    res = 0
    for i, (cvx, cvy) in enumerate(compacted_coordinates):
        for cwx, cwy in compacted_coordinates[i+1:]:
            # Check eligibility
            eligible = True
            for cny in range(min(cvy, cwy), max(cvy, cwy)+1):
                for cnx in range(min(cvx, cwx), max(cvx, cwx)+1):
                    if (compacted_grid[cny][cnx] is not None) and (compacted_grid[cny][cnx] == 'O'):
                        eligible = False
                        break
                else:
                    continue
                break
            if eligible:
                ovx, ovy = oxs[cvx], oys[cvy]
                owx, owy = oxs[cwx], oys[cwy]
                res = max(res, (abs(ovx-owx)+1) * (abs(ovy-owy)+1))

    return res


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

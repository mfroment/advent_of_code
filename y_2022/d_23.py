import time
import aoc.utils as aocu


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    return sections[0]


def parse_elves(values):
    ps = set()
    h = len(values)
    w = len(values[0])
    for j in range(h):
        for i in range(w):
            if values[j][i] == "#":
                ps.add((i, j))
    return ps


def p_add(p, q):
    px, py = p
    qx, qy = q
    return (px + qx, py + qy)


LOOK = [
    {(0, -1): {(0, -1), (-1, -1), (1, -1)}},
    {(0, 1): {(0, 1), (-1, 1), (1, 1)}},
    {(-1, 0): {(-1, 0), (-1, 1), (-1, -1)}},
    {(1, 0): {(1, 0), (1, 1), (1, -1)}},
]


def new_p(p, ps, look):
    dp, dqs = next(iter(look.items()))
    cannot_move = any(p_add(p, dq) in ps for dq in dqs)
    if cannot_move:
        return p
    else:
        return p_add(p, dp)


def has_neighbours(p, ps):
    DQS = {(0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1)}
    qs = {p_add(p, dq) for dq in DQS}
    return any(n in ps for n in qs)


def solve(values):
    part_1 = None
    ps = parse_elves(values)
    i = 0
    while True:
        # print(i, len(ps))
        # print(ps)
        new_ps = dict()
        collision_count = dict()
        all_no_neighbours = True
        for p in ps:
            if not has_neighbours(p, ps):
                new_ps[p] = p
            else:
                all_no_neighbours = False
                tmp_new_p = p
                for j in range(4):
                    tmp_new_p = new_p(p, ps, LOOK[(i + j) % 4])
                    if tmp_new_p != p:
                        break
                new_ps[p] = tmp_new_p
            collision_count.setdefault(new_ps[p], 0)
            collision_count[new_ps[p]] += 1
        if all_no_neighbours:
            break
        for p in ps:
            if collision_count[new_ps[p]] > 1:
                new_ps[p] = p
        ps = set(new_ps.values())
        i = (i + 1)
        if i == 10:
            part_1 = compute_solve_1(ps)

    return part_1, i + 1


def compute_solve_1(ps):
    lx = min(x for (x, y) in ps)
    ly = min(y for (x, y) in ps)
    ux = max(x for (x, y) in ps)
    uy = max(y for (x, y) in ps)
    area = (ux - lx + 1) * (uy - ly + 1)
    return area - len(ps)


def main():
    input_values = parse_input()

    start_time = time.time()
    part_1, part_2 = solve(input_values)
    print(f"Part 1: {str(part_1):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    print(f"Part 2: {str(part_2):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

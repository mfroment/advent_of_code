import itertools
import time

import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            s, e = line.split("~")
            s = tuple(int(v) for v in s.split(","))
            e = tuple(int(v) for v in e.split(","))
            r = tuple((min(s[i], e[i]), max(s[i], e[i])) for i in range(3))
            sub_res.append(tuple(r))
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def resolve_initial_fall(bricks):
    surface = dict()
    bricks = sorted(bricks, key=lambda b: b[2][0])
    structure = dict()
    for brick in bricks:
        contacts = set()
        contact_z = 0
        for x, y in itertools.product(range(brick[0][0], brick[0][1] + 1), range(brick[1][0], brick[1][1] + 1)):
            if (x, y) in surface:
                if surface[(x, y)][2][1] == contact_z:
                    contacts.add(surface[(x, y)])
                elif surface[(x, y)][2][1] > contact_z:
                    contacts = {surface[(x, y)]}
                    contact_z = surface[(x, y)][2][1]
        fallen_brick = (
            brick[0],
            brick[1],
            (contact_z + 1, contact_z + 1 + brick[2][1] - brick[2][0]),
        )
        structure[fallen_brick] = contacts
        for x, y in itertools.product(range(brick[0][0], brick[0][1] + 1), range(brick[1][0], brick[1][1] + 1)):
            surface[(x, y)] = fallen_brick
    return structure


def solve_1(values):
    structure = resolve_initial_fall(values)
    unsafe = set()
    for contacts in structure.values():
        if len(contacts) == 1:
            unsafe.add(next(iter(contacts)))  # :(
    return len(structure) - len(unsafe)


def solve_2(values):
    structure = resolve_initial_fall(values)
    supporting = {b: set() for b in structure}
    for b, contacts in structure.items():
        for c in contacts:
            supporting[c] |= {b}

    def get_falling(bricks):
        supported = set()
        for b in bricks:
            supported |= supporting[b]
        new_bricks = set()
        for b in supported - bricks:
            contacts = structure[b]
            if contacts and not (contacts - bricks):
                new_bricks.add(b)
        if not new_bricks:
            return bricks
        return get_falling(bricks | new_bricks)

    return sum(len(get_falling({b})) - 1 for b in structure)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

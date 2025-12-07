import time

import aoc.utils as aocu

import functools


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [c for c in line]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    splits = 0
    prev = { values[0].index('S') }
    for row in values[1:]:
        current = set()
        for i, c in enumerate(row):
            if i in prev:
                if c == '.':
                    current.add(i)
                elif c == '^':
                    assert 0 < i < len(values[0])-1
                    current |= {i-1, i+1}
                    splits += 1
                else:
                   raise ValueError()
        prev = current        
    return splits


def solve_2(values):
    @functools.cache
    def subworlds(depth, pos):
        if depth == len(values):
            return 1
        if values[depth][pos] == '.':
            res = subworlds(depth+1, pos)
        elif values[depth][pos] == '^':
            assert 0 < pos < len(values[0])-1
            res = subworlds(depth+1, pos-1) + subworlds(depth+1, pos+1)
        else:
            raise ValueError(values[depth][pos])
        return res

    return subworlds(1, values[0].index('S'))

def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

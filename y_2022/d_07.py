import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r"\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


def compute_sizes(values):
    # add a fake `cd` instruction in order to "force close" the parsing of `ls` if that's the last non-fake instruction
    values.append(['$', 'cd', '/'])
    # process instructions as a stack easier with a stack (pop from tail rather than head), thus reverse:
    values = list(reversed(values))

    dir_sizes = dict()
    current_dir = None
    while len(values) > 0:
        v = values.pop()
        if v[0] == '$':
            if v[1] == 'cd':
                if v[2] == '/':
                    current_dir = '/'
                elif v[2] == '..':
                    current_dir = '/' + '/'.join(current_dir[1:].split('/')[:-1])
                else:
                    current_dir = current_dir + ('' if current_dir == '/' else '/') + v[2]
                dir_sizes.setdefault(current_dir, 0)
            elif v[1] == 'ls':
                # ls mode - compute (non-recursive) size (no need to bother if already visited, or record subdirs)
                dir_sizes[current_dir] = 0
                while len(values) > 0:
                    v = values.pop()
                    if v[0] == '$':
                        # next command, push it back then exit ls mode
                        values.append(v)
                        break
                    # if file, add its size, otherwise, skip
                    if isinstance(v[0], int):
                        dir_sizes[current_dir] += v[0]

    # this is ridiculously inefficient (O(n^2)) except for getting the solution quicker
    dir_recursive_sizes = dict()
    for dir in dir_sizes:
        recursive_size = 0
        for subdir, subsize in dir_sizes.items():
            if subdir[:len(dir)] == dir:
                recursive_size += subsize
        dir_recursive_sizes[dir] = recursive_size

    return dir_recursive_sizes


def solve_1(recursive_sizes):
    return sum(s for s in recursive_sizes.values() if s <= 100000 )


def solve_2(recursive_sizes):
    deletion_target = recursive_sizes["/"] - 40000000
    return min(s for s in recursive_sizes.values() if s >= deletion_target)


if __name__ == "__main__":
    input_values = parse_input()

    recursive_sizes = compute_sizes(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(recursive_sizes)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(recursive_sizes)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

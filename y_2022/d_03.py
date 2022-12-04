import time
import aoc.utils as aocu
import string


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [line]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)


ITEMS = string.ascii_lowercase + string.ascii_uppercase
PRIORITIES = {l: ITEMS.index(l) + 1 for l in ITEMS}


def common_item(*sets):
    candidates = set.intersection(*sets)
    assert (len(candidates) == 1)
    return candidates.pop()


def solve_1(values):
    total_priority = 0
    for v in values:
        c = common_item(set(v[:len(v) // 2]), set(v[len(v) // 2:]))
        total_priority += PRIORITIES[c]
    return total_priority


def solve_2(values):
    total_priority = 0
    for i in range(0, len(values) // 3):
        c = common_item(set(values[3 * i]), set(values[3 * i + 1]), set(values[3 * i + 2]))
        total_priority += PRIORITIES[c]
    return total_priority


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

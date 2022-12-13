import time
import aoc.utils as aocu
from ast import literal_eval
from functools import cmp_to_key


def parse_input(file=__file__, prefix=None):
    sections = aocu.read_input(file, prefix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            sub_res.append(literal_eval(line))
        res.append(sub_res)
    return res


# -1, 0, 1 depending on a < b, a == b, a > b
def int_cmp(a, b):
    return (a > b) - (a < b)


def packet_cmp(a, b):
    # a, b are possibly int
    match isinstance(a, int), isinstance(b, int):
        case True, True:
            return int_cmp(a, b)
        case True, False:
            return packet_cmp([a], b)
        case False, True:
            return packet_cmp(a, [b])
    # a, b are both lists
    match len(a) == 0, len(b) == 0:
        case True, True:
            return 0
        case True, False:
            return -1
        case False, True:
            return 1
    # a, b are both non-empty lists
    cmp_first = packet_cmp(a[0], b[0])
    if cmp_first != 0:
        return cmp_first
    else:
        return packet_cmp(a[1:], b[1:])


def solve_1(packet_pairs):
    res = 0
    for idx, (a, b) in enumerate(packet_pairs):
        if packet_cmp(a, b) == -1:
            res += idx + 1
    return res


def solve_2(packet_pairs):
    packets = [packet for pair in packet_pairs for packet in pair]
    packets.extend([[[2]], [[6]]])
    packets.sort(key=cmp_to_key(packet_cmp))
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

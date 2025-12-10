import time
import aoc.utils as aocu
import numpy as np

SNAFU = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}

REVERSE_SNAFU = {
    "0": "=",
    "1": "-",
    "2": "0",
    "3": "1",
    "4": "2",
}


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    return sections[0]


def sna_2_dec(sna):
    dec = 0
    for exponent, dec_digit in enumerate(reversed(sna)):
        dec += (5**exponent) * SNAFU[dec_digit]
    return dec


def dec_2_sna(dec):
    exponent = 0
    while (dec - 5**exponent) >= 0:
        dec += 2 * (5**exponent)
        exponent += 1
    sna = "".join(REVERSE_SNAFU[c] for c in str(np.base_repr(dec, base=5)))
    return sna


def solve_1(values):
    dec_total = sum(sna_2_dec(sna) for sna in values)
    return dec_2_sna(dec_total)


def solve_2(values):
    return "Start the blender!"


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

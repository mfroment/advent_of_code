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
    return aocu.reduce_input(res)  # dimensionality reduction


def process(instructions):
    x = [1]
    screen = [' ' for _ in range(0, 240)]

    def cycle_update():
        cursor = len(x) - 1
        if x[-1] - 1 <= cursor % 40 <= x[-1] + 1:
            screen[cursor] = '█'
        x.append(x[-1])

    for instruction in instructions:
        if instruction[0] == 'noop':
            cycle_update()
        elif instruction[0] == 'addx':
            cycle_update()
            cycle_update()
            x[-1] += instruction[1]
        else:
            raise (ValueError(f"Unknown instruction: {instruction[0]}"))
    return x, screen


def solve_1(x):
    return sum(x[c] * (c + 1) for c in range(19, len(x), 40))


def solve_2(screen):
    return '\n' + '\n'.join([''.join(screen[i:i + 40]) for i in range(0, 240, 40)])


if __name__ == "__main__":
    input_values = parse_input()

    x, screen = process(input_values)

    start_time = time.time()
    print(f"Part 1: {str(solve_1(x)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(screen)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    print("(this should read: RZHFGJCB")

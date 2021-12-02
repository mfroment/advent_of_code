from pathlib import Path


def solve_1(commands):
    depth = 0
    position = 0
    for (direction, value) in commands:
        if direction == "up":
            depth -= value
            if depth < 0:
                depth = 0
        elif direction == "down":
            depth += value
        else:
            position += value
    return depth * position


def solve_2(commands):
    depth = 0
    position = 0
    aim = 0
    for (direction, value) in commands:
        if direction == "up":
            aim -= value
        elif direction == "down":
            aim += value
        else:
            position += value
            depth += aim*value
            if depth < 0:
                depth = 0
    return depth * position


if __name__ == "__main__":
    p = Path(__file__)
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        input_commands = [(lambda a, b: [a, int(b)])(*r.split(' ')) for r in f.readlines() if r != '']

    print("Part 1:", solve_1(input_commands))
    print("Part 2:", solve_2(input_commands))

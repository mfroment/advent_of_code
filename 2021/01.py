from pathlib import Path
from collections import deque


def solve(depths, window_size):
    prev = deque()
    count = 0
    for d in depths:
        if len(prev) >= window_size:
            if d > prev.popleft():
                count += 1
        prev.append(d)
    return count


if __name__ == "__main__":
    p = Path(__file__)
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        input_depths = [int(d) for d in f.read().split('\n')]

    print("Part 1:", solve(input_depths, 1))
    print("Part 2:", solve(input_depths, 3))

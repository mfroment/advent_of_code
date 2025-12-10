import time
from pathlib import Path

P = Path(__file__)
INPUT_FILE = P.parent.joinpath("input").joinpath(P.stem[:4] + ".txt")


one_1 = sum(
    (lambda a, b, c, d: (a - c) * (d - b) >= 0)(*x)
    for x in map(
        lambda *x: x,
        *([iter(int(n) for l in open(INPUT_FILE).readlines() for m in l.split(",") for n in m.split("-"))] * 4),
    )
)
one_2 = sum(
    (lambda a, b, c, d: b >= c and a <= d)(*x)
    for x in map(
        lambda *x: x,
        *([iter(int(n) for l in open(INPUT_FILE).readlines() for m in l.split(",") for n in m.split("-"))] * 4),
    )
)

if __name__ == "__main__":
    start_time = time.time()
    print(f"Part 1: {str(one_1):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(one_2):<30}{'(':>30}{time.time() - start_time:.3f}s)")

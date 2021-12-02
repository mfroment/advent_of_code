from pathlib import Path

SUM = 2020
input = dict()
p = Path(__file__)
with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
    while True:
        v = f.readline()
        if not v:
            break
        v = int(v)
        if v in input:
            print(f"{v}*{SUM - v}={v * (SUM - v)}")
            exit()
        input[SUM - v] = v

print("No solution found")

from pathlib import Path
import re


def parse_input(file=__file__):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ".txt")) as f:
        for r in f.readlines():
            m = re.search(r"(\d+)-(\d+) (.): (\w+)", r)
            res.append(
                {
                    "min": int(m.group(1)),
                    "max": int(m.group(2)),
                    "char": m.group(3),
                    "password": m.group(4),
                }
            )
    return res


def solve_1(values):
    count = 0
    for v in values:
        char_count = v["password"].count(v["char"])
        if char_count >= v["min"] and char_count <= v["max"]:
            count += 1
    return count


def solve_2(values):
    count = 0
    for v in values:
        c1 = v["password"][v["min"] - 1]
        c2 = v["password"][v["max"] - 1]
        if (c1 == v["char"] or c2 == v["char"]) and c1 != c2:
            count += 1
    return count


if __name__ == "__main__":
    inputs = parse_input()

    print("Part 1:", solve_1(inputs))
    print("Part 2:", solve_2(inputs))

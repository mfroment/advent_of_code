from pathlib import Path
import re


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        current = dict()
        for r in f.readlines() + [""]:  # add terminator
            if r.strip() == "":
                res.append(current)
                current = dict()
                continue
            for p in r.strip().split(" "):
                k, v = p.split(":")
                current[k] = v
        return res


def is_valid_1(p):
    return len(p) == 8 or (len(p) == 7 and "cid" not in p)


def is_numeric(s, lb, ub):
    return re.search(r"^\d+$", s) and lb <= int(s) <= ub


def is_valid_2(p):
    if not is_valid_1(p):
        return False
    if (
        not is_numeric(p["byr"], 1920, 2002)
        or not is_numeric(p["iyr"], 2010, 2020)
        or not is_numeric(p["eyr"], 2020, 2030)
    ):
        return False
    m = re.search(r"^(\d+)(in|cm)", p["hgt"])
    if (
        not m
        or (m.group(2) == "cm" and not is_numeric(m.group(1), 150, 193))
        or (m.group(2) == "in" and not is_numeric(m.group(1), 59, 76))
    ):
        return False
    if not re.search(r"^#[0-9a-f]{6}$", p["hcl"]):
        return False
    if not p["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False
    if not re.search(r"^[0-9]{9}$", p["pid"]):
        return False
    return True


def solve_1(values):
    return sum([1 if is_valid_1(p) else 0 for p in values])


def solve_2(values):
    return sum([1 if is_valid_2(p) else 0 for p in values])


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

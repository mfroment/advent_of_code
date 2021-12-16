from pathlib import Path


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                continue
            res.append(r.strip())
        return res


def binarize(s, zero):
    return int(''.join(['0' if c == zero else '1' for c in s]), 2)


def seat(s):
    r, c = binarize(s[:7], 'F'), binarize(s[7:], 'L')
    return r, c, r * 8 + c


def solve_1(values):
    return max([seat(s)[2] for s in values])


def solve_2(values):
    seats = {seat(s)[2] for s in values}
    min_id, max_id = min(seats), max(seats)
    expected_sum = (max_id * (max_id + 1) - (min_id - 1) * min_id) // 2
    actual_sum = sum(seats)
    return expected_sum - actual_sum


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

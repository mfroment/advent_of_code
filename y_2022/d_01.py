from pathlib import Path
import time


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    res = []
    chunk = []
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines():
            if r.strip() == '':
                if len(chunk) > 0:
                    res.append(chunk)
                chunk = []
                continue
            chunk.append(int(r.strip()))
        if len(chunk) > 0:
            res.append(chunk)
        return res


def sorted_sums(values):
    return list(reversed(sorted([sum(v) for v in values])))


def solve_1(values):
    return sorted_sums(values)[0]


def solve_2(values):
    return sum(sorted_sums(values)[0:3])


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

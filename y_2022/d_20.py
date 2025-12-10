import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for line in sections[0]:
        res.append(aocu.s2i(line))
    return res


def get_mixorder(values):
    return [i for i in range(len(values))]


def mix(values, mixorder):
    values = values[:]
    for j in range(len(values)):
        i = mixorder.index(j)
        shift = values[i]
        if shift == 0:
            continue
        if shift > 0:
            new_i = (i + shift - 1) % (len(values) - 1) + 1
        else:  # values[i] <0:
            new_i = (i + shift) % (len(values) - 1)
        mixorder = mixorder[:i] + mixorder[i + 1 :]
        values = values[:i] + values[i + 1 :]
        values = values[:new_i] + [shift] + values[new_i:]
        mixorder = mixorder[:new_i] + [j] + mixorder[new_i:]
    return values, mixorder


def score(values):
    zero_i = values.index(0)
    a = values[(zero_i + 1000) % len(values)]
    b = values[(zero_i + 2000) % len(values)]
    c = values[(zero_i + 3000) % len(values)]
    return sum(values[(zero_i + i * 1000) % len(values)] for i in [1, 2, 3])


def solve_1(values):
    mixorder = get_mixorder(values)
    values, _ = mix(values, mixorder)
    return score(values)


def solve_2(values):
    values = [v * 811589153 for v in values]
    mixorder = get_mixorder(values)
    for _ in range(10):
        values, mixorder = mix(values, mixorder)
    return score(values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

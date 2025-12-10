import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            parts = [part.strip() for part in line.split(":")[1].split("|")]
            sep = re.compile(r"\s*(\S+)\s*")
            parts = [[int(elem) for elem in re.findall(sep, part)] for part in parts]
            sub_res.append(parts)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    scores = []
    for wins, haves in values:
        s = sum(1 for v in haves if v in wins)
        scores.append(s)
    return sum(2 ** (s - 1) for s in scores if s > 0)


def solve_2(values):
    n_cards = [1 for _ in range(len(values))]
    for i, (wins, haves) in enumerate(values):
        s = sum(1 for v in haves if v in wins)
        for j in range(i + 1, min(i + s + 1, len(values) + 1)):
            n_cards[j] += n_cards[i]

    return sum(n_cards)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.6f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.6f}s)")


if __name__ == "__main__":
    main()

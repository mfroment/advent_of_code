import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r"\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def extrapolate_seq(seq):
    cseq = seq[:]
    subseqs = [cseq]
    while any(s != 0 for s in cseq):
        cseq = [cseq[i] - cseq[i - 1] for i in range(1, len(cseq))]
        subseqs += [cseq]
    for i in range(-2, -len(subseqs) - 1, -1):
        subseqs[i].append(subseqs[i][-1] + subseqs[i + 1][-1])
    return subseqs[0][-1]


def solve_1(values):
    return sum(extrapolate_seq(seq) for seq in values)


def solve_2(values):
    return sum(extrapolate_seq(list(reversed(seq))) for seq in values)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

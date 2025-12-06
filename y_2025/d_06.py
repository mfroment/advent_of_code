import re
import time

import aoc.utils as aocu
import math


def parse_input_1(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line.strip(), maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    res = aocu.reduce_input(res)  # dimensionality reduction
    operators = res[-1]
    numbers = [[v[i] for v in res[:-1]] for i in range(len(operators))]
    return numbers, operators


def parse_input_2(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    unparsed_numbers = sections[0][:-1]
    unparsed_operators = sections[0][-1]

    operators = []
    positions = []
    for i, c in enumerate(unparsed_operators):
        if c != ' ':
            positions.append(i)
            operators.append(c)

    n_problems = len(positions)
    positions.append(len(unparsed_operators)+1) # add terminator
    numbers = []
    for i in range(n_problems):
        problem_numbers = []
        pos_start = positions[i]
        pos_len = positions[i+1]-positions[i]-1
        number_stack = [list() for _ in range(pos_len)]
        for pos in range(pos_start, pos_start+pos_len):
            for unparsed_number_row in unparsed_numbers:
                number_stack[pos - pos_start].append(unparsed_number_row[pos])
        for number_figures in number_stack:
            problem_numbers.append(int(''.join(number_figures).rstrip()))
        numbers.append(problem_numbers)
    return numbers, operators


def solve(values):
    numbers, operators = values
    problems = []
    for i in range(len(operators)):
        vs = numbers[i]
        operand = operators[i]
        if operand == '+':
            problems.append(sum(vs))
        elif operand == '*':
            problems.append(math.prod(vs))
        else:
            raise ValueError(f"Unknown operand: {operand}")
    return sum(problems)


def main():

    start_time = time.time()
    input_values_1 = parse_input_1()
    print(f"Part 1: {str(solve(input_values_1)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

    start_time = time.time()
    input_values_2 = parse_input_2()
    print(f"Part 2: {str(solve(input_values_2)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

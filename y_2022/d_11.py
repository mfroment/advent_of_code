import time
import re
import aoc.utils as aocu
import math


class Monkey:
    def __init__(self, items, operations, test_div, true_monkey, false_monkey):
        self.inspections = 0
        self.items = items
        self.operations = operations
        self.test_div = test_div
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

    def inspect(self, monkeys):
        self.inspections += len(self.items)
        old_items = self.items[:]
        self.items = []
        for item in old_items:
            for op in self.operations:
                item = op(item)
            if item % self.test_div == 0:
                monkeys[self.true_monkey].receive(item)
            else:
                monkeys[self.false_monkey].receive(item)

    def receive(self, item):
        self.items.append(item)


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    monkeys = []
    operation_strings = []
    for i, section in enumerate(sections):
        sub_res = []
        for line in section:
            tokens = re.split(r"\s+", line, maxsplit=0)
            tokens = [t.replace(',', '') for t in tokens]
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        items = sub_res[1][3:]
        # Note: To understand the code below and the use of "dummy" string array & dummy lambda input i, see this:
        #       https://stackoverflow.com/questions/2295290/what-do-lambda-function-closures-capture
        #       THIS DOES NOT WORK:
        #         operation_string = ' '.join(str(x) for x in sub_res[2][4:])
        #         operations = [lambda old, i=i: eval(operation_string.replace('old', str(old)))]
        #       (the lambda defined "last" will be the one used everywhere)
        operation_strings.append(' '.join(str(x) for x in sub_res[2][4:]))
        operations = [lambda old, i=i: eval(operation_strings[i].replace('old', str(old)))]
        test_div = sub_res[3][4]
        true_monkey = sub_res[4][6]
        false_monkey = sub_res[5][6]
        monkey = Monkey(items, operations, test_div, true_monkey, false_monkey)
        monkeys.append(monkey)
    return monkeys


def iterate_once(monkeys):
    for m in monkeys:
        m.inspect(monkeys)


def solve(monkeys, n_iterations, extra_operation):
    for m in monkeys:
        m.operations.append(extra_operation)
    for _ in range(n_iterations):
        iterate_once(monkeys)
    inspections = [m.inspections for m in monkeys]
    x, y = sorted(inspections)[-2:]
    return x * y


def solve_1(monkeys):
    return solve(monkeys, 20, lambda x: x // 3)


def solve_2(monkeys):
    lcm = math.lcm(*(m.test_div for m in monkeys))
    return solve(monkeys, 10000, lambda x: x % lcm)


if __name__ == "__main__":
    input_values = parse_input()
    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

    input_values = parse_input()
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

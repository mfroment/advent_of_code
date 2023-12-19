import time
import re
import aoc.utils as aocu
from functools import reduce


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)

    workflows = {}
    for line in sections[0]:
        name, rest = line[:-1].split("{")
        checks = []
        for t in rest.split(","):
            checks.append(t.split(":"))
        checks[-1] = ['True', checks[-1][0]]
        workflows[name] = checks

    ratings = []
    for line in sections[1]:
        line = re.sub(r"(.)=",r"'\1':",line)
        ratings.append(eval(line))

    return workflows, ratings

def process_part(part, workflow_id, workflows):
    x, m, a, s = part['x'], part['m'], part['a'], part['s']

    workflow = workflows[workflow_id]
    for check in workflow:
        condition = eval(check[0])
        if condition:
            outcome = check[1]
            if outcome == 'R':
                return 0
            elif outcome == 'A':
                return x+m+a+s
            else:
                return process_part(part, outcome, workflows)


def solve_1(values):
    workflows, parts = values
    return sum([process_part(part, 'in', workflows) for part in parts])

#--------------------------------------------

def duplicate_part_range(part_range):
    return { k: v[:] for k, v in part_range.items() }


def check_part_range(part_range, condition):
    # return: t = part range that satisfies condition, f = part range that does not
    #         None when respective side of the conditon is not satisfiable
    if condition == 'True':
        return part_range, None
    
    var, op, val = condition[0], condition[1], int(condition[2:])
    lb, ub = part_range[var]
    if op == '<':
        if ub < val:
            return part_range, None
        elif lb < val:
            t = duplicate_part_range(part_range)
            f = duplicate_part_range(part_range)
            t[var][1] = val-1
            f[var][0] = val
            return t, f
        else:
            return None, part_range
    if op == '>':
        if lb > val:
            return part_range, None
        elif ub > val:
            t = duplicate_part_range(part_range)
            f = duplicate_part_range(part_range)
            t[var][0] = val+1
            f[var][1] = val
            return t, f
        else:
            return None, part_range
    assert False


def process_part_range(part_range, workflow_id, workflows):
    workflow = workflows[workflow_id]
    res = []
    # t = part range that satisfies the condition, f = part range that does not
    # we treat t according to the outcome, and f is passed on to the next check (if any)
    t, f = None, part_range
    for check in workflow:
        if f is None:
            break
        t, f = check_part_range(f, check[0])
        outcome = check[1]
        if t is None:
            continue
        if outcome == 'R':
            pass
        elif outcome == 'A':
            res.append(t)
        else:
            res += process_part_range(t, outcome, workflows)
    return res
            

def solve_2(values):
    workflows, _ = values
    part_range = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    res = process_part_range(part_range, 'in', workflows)
    return sum(reduce(lambda x, y: x*(y[1]-y[0]+1), r.values(), 1) for r in res)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

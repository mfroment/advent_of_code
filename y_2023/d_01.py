import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def solve_1(values):
    res = [ re.sub("[a-z]", "", v) for v in values ]
    res = [ int(r[0])*10 + int(r[-1]) for r in res ]
    return sum(res)


def solve_2(values):
    def parse(v):
        FIGURES = {k: i for i, k in enumerate(('zero', 'one','two','three','four','five','six','seven','eight','nine'))}
        
        l = None
        vl = v
        while l is None:
            if vl[0].isnumeric():
                l = int(vl[0])
            for k, i in FIGURES.items():
                vl.startswith(k)
                if str(vl).startswith(k):
                    l = i
                    break
            if l is not None:
                break
            vl = vl[1:]
        r = None
        vr = v
        while r is None:
            if vr[-1].isnumeric():
                r = int(vr[-1])
            for k, i in FIGURES.items():
                if vr.endswith(k):
                    r = i
                    break
            if r is not None:
                break
            vr = vr[:-1]
        return l*10 + r    

    res = [ parse(v) for v in values ]
    return sum(res)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

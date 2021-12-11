from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    res = []
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        for r in f.readlines():
            if r == '':
                pass
            parts = r.strip().split(' | ')
            digit_patterns = [''.join(sorted(p)) for p in parts[0].split(' ')]
            number_patterns = [''.join(sorted(p)) for p in parts[1].split(' ')]
            res.append([digit_patterns, number_patterns])
    return res


# --- Part 1 ---
def solve_1(values):
    count = 0
    for _, number_patterns in values:
        for np in number_patterns:
            if len(np) in {7, 4, 3, 2}:
                count += 1
    return count


# --- Part 2 ---
def decode_digits(digit_patterns):
    digits = {pattern: None for pattern in digit_patterns}
    dp_1478 = dict()
    dp_235 = set()
    dp_069 = set()
    # Assign digits to patterns based on length when possible
    pattern_length_to_digit = {7: 8, 2: 1, 4: 4, 3: 7}
    for dp in digits:
        if len(dp) in pattern_length_to_digit:
            digit = pattern_length_to_digit[len(dp)]
            digits[dp] = digit
            dp_1478[digit] = set(dp)
        elif len(dp) == 5:
            dp_235.add(dp)
        else:
            assert len(dp) == 6  # Sanity check
            dp_069.add(dp)
    # Figure out the remaining cases from the above
    for dp in dp_235:
        pset = set(dp)
        if len(pset & dp_1478[1]) == 2:
            digits[dp] = 3
        elif len(pset & dp_1478[4]) == 3:
            digits[dp] = 5
        else:
            digits[dp] = 2
    for dp in dp_069:
        pset = set(dp)
        if len(pset & dp_1478[1]) == 1:
            digits[dp] = 6
        elif len(pset & dp_1478[4]) == 4:
            digits[dp] = 9
        else:
            digits[dp] = 0
    return digits


def compute_number(digits, number_patterns):
    number = 0
    for np in number_patterns:
        number = 10 * number + digits[np]
    return number


def solve_2(values):
    res = 0
    for digit_patterns, number_patterns in values:
        digits = decode_digits(digit_patterns)
        res += compute_number(digits, number_patterns)
    return res


if __name__ == "__main__":
    input_patterns = parse_input()

    print("Part 1:", solve_1(input_patterns))
    print("Part 2:", solve_2(input_patterns))

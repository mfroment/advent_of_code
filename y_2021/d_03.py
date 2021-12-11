from pathlib import Path


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem + '.txt')) as f:
        return [[int(a) for a in r.strip()] for r in f.readlines() if r != '']


def bitarray_to_int(bit):
    str_rep = "".join([str(b) for b in bit])
    return int(str_rep, 2)


def solve_1(bitarrays):
    gamma = [0] * len(bitarrays[0])
    for bitarray in bitarrays:
        for i, bit in enumerate(bitarray):
            gamma[i] += bit
    epsilon = []
    for i, bitsum in enumerate(gamma):
        gamma[i] = 1 if bitsum >= len(bitarrays) / 2 else 0
        epsilon.append(1 - gamma[i])
    return bitarray_to_int(gamma) * bitarray_to_int(epsilon)


def select_common(bitarrays, most_common, pos=0):
    # There should always be some input bitarrays:
    assert bitarrays
    if pos == len(bitarrays[0]):
        return bitarrays
    count = 0
    for bitarray in bitarrays:
        if bitarray[pos] == 1:
            count += 1
    if count == len(bitarrays):
        selected_value = 1
    elif count == 0:
        selected_value = 0
    else:
        selected_value = 1 if 2 * count >= len(bitarrays) else 0
        if not most_common:
            selected_value = 1 - selected_value
    selected_bitarrays = []
    for bitarray in bitarrays:
        if bitarray[pos] == selected_value:
            selected_bitarrays.append(bitarray)
    return select_common(selected_bitarrays, most_common, pos + 1)


def solve_2(bits):
    oxygen = select_common(bits, True)
    dioxyde = select_common(bits, False)
    # There should be only 1 element resulting from selecting bitarrays with
    # either criterion:
    assert len(oxygen) == 1 and len(dioxyde) == 1
    return bitarray_to_int(oxygen[0]) * bitarray_to_int(dioxyde[0])


if __name__ == "__main__":
    input_bitarrays = parse_input()

    print("Part 1:", solve_1(input_bitarrays))
    print("Part 2:", solve_2(input_bitarrays))

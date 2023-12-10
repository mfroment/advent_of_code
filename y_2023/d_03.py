import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = [aocu.s2i(t) for t in list(line)]
            sub_res.append(tokens)
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def pad_grid(values):
    padded = []
    width = len(values[0])
    padded.append(['.']*(width+2))
    for v in values:
        padded.append(['.'] + v + ['.'])
    padded.append(['.']*(width+2))

    return padded


def get_numbers(values):  
    numbers = dict()
    for j, line in enumerate(values):
        # initialize for the line
        nb_pos = None
        nb_value = None
        for i, cell in enumerate(line):
            if isinstance(cell, int):
                if nb_value is None:
                    # start of a number
                    nb_pos = (i, j)
                    nb_value = cell
                else:
                    # continuation of a number
                    nb_value = nb_value*10 + cell
            elif nb_value is not None:
                # end of a number
                numbers[nb_pos]= nb_value
                nb_pos = None
                nb_value = None
    return numbers


def get_number_neighbors(pos, n, values):
    n_length = len(str(n))
    i, j = pos
    neighbors = dict()
    # this revisits the cells occupied by the number itself, but it's ok (skip if int)
    for nbng_j in (j-1, j, j+1):
        for nbng_i in range(i-1, i+n_length+1):
            nbng_value = values[nbng_j][nbng_i]
            if nbng_value != '.' and not(isinstance(nbng_value, int)):
                neighbors[(nbng_i, nbng_j)] = nbng_value
                break
    return neighbors
    

def solve_1(values):
    values = pad_grid(values)
    numbers = get_numbers(values)

    part_numbers = []

    for nb_pos, nb_value in numbers.items():
        neighbors = get_number_neighbors(nb_pos, nb_value, values)
        if neighbors:
            part_numbers.append(nb_value)
    return sum(part_numbers)


def solve_2(values):
    values = pad_grid(values)
    numbers = get_numbers(values)

    gears = {}

    numbers = get_numbers(values)
    for nb_pos, nb_value in numbers.items():
        neighbors = get_number_neighbors(nb_pos, nb_value, values)
        for nbng_pos, nbng_value in neighbors.items():
            if nbng_value == '*':
                gears.setdefault(nbng_pos, []).append(nb_value)

    return sum([g[0]*g[1] for g in gears.values() if len(g) == 2])


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

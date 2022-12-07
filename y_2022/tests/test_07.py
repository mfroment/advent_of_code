from y_2022.d_07 import *

input_values = parse_input(__file__)
recursive_sizes = compute_sizes(input_values)


def test_1():
    assert solve_1(recursive_sizes) == 95437


def test_2():
    assert solve_2(recursive_sizes) == 24933642

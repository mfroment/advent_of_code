from y_2022.d_15 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1_naive(input_values, 10) == 26
    assert solve_1_faster(input_values, 10) == 26


def test_2():
    assert solve_2_slow(input_values, 0, 20, 0, 20) == 56000011

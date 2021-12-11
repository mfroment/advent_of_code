from y_2021.d_11 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values, 0) == 0
    assert solve_1(input_values, 1) == 0
    assert solve_1(input_values, 2) == 35
    assert solve_1(input_values, 10) == 204
    assert solve_1(input_values, 100) == 1656


def test_2():
    assert solve_2(input_values) == 195

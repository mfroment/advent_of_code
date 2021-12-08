from y_2021.d_08 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == 26


def test_2():
    assert solve_2(input_values) == 61229

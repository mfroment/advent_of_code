from y_2022.d_09 import *

input_values_1 = parse_input(__file__, "1")
input_values_2 = parse_input(__file__, "2")


def test_1():
    assert solve_1(input_values_1) == 13


def test_2():
    assert solve_2(input_values_1) == 1
    assert solve_2(input_values_2) == 36

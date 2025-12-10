from y_2021.d_12 import *

input_values_1 = parse_input(__file__, "1")
input_values_2 = parse_input(__file__, "2")
input_values_3 = parse_input(__file__, "3")


def test_1():
    assert solve_1(input_values_1) == 10
    assert solve_1(input_values_2) == 19
    assert solve_1(input_values_3) == 226


def test_2():
    assert solve_2(input_values_1) == 36
    assert solve_2(input_values_2) == 103
    assert solve_2(input_values_3) == 3509

from y_2021.d_11 import *

input_values_1 = parse_input(__file__, '1')
input_values_1_1 = parse_input(__file__, '1.1')
input_values_1_2 = parse_input(__file__, '1.2')
input_values_2 = parse_input(__file__, '2')


def test_1():
    assert solve_1(input_values_1, 0) == 0
    assert solve_1(input_values_1, 1) == 9
    assert solve_1(input_values_1, 2) == 9

    # now modifying input_values_1:
    apply_step(input_values_1)
    assert input_values_1 == input_values_1_1
    apply_step(input_values_1)
    assert input_values_1 == input_values_1_2

    assert solve_1(input_values_2, 0) == 0
    assert solve_1(input_values_2, 1) == 0
    assert solve_1(input_values_2, 2) == 35
    assert solve_1(input_values_2, 10) == 204
    assert solve_1(input_values_2, 100) == 1656


def test_2():
    assert solve_2(input_values_2) == 195

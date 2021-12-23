from y_2021.d_22 import *

input_values_1 = parse_input(__file__, '1')
input_values_2 = parse_input(__file__, '2')
input_values_3 = parse_input(__file__, '3')

def test_1():
    assert solve_1(input_values_1) == 39
    assert solve_1(input_values_2) == 590784


def test_2():
    assert solve_2(input_values_3) == 2758514936282235

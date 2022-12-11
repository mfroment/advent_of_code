from y_2022.d_11 import *

def test_1():
    input_values = parse_input(__file__)
    assert solve_1(input_values) == 10605


def test_2():
    input_values = parse_input(__file__)
    assert solve_2(input_values) == 2713310158

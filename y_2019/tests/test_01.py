from y_2019.d_01 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == 33583


def test_2():
    assert solve_2(input_values) == 50346

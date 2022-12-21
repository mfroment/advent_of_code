from y_2022.d_21 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == 152


def test_2():
    assert solve_2_search(input_values) == 301
    assert solve_2_symbolic(input_values) == 301

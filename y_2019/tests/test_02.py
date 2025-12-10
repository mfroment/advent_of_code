from y_2019.d_02 import *

input_values = parse_input(__file__)


def test_1():
    process(input_values)
    assert input_values == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]


def test_2():
    assert solve_2(input_values) == None

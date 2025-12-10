from y_2022.d_05 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == "CMZ"


def test_2():
    assert solve_2(input_values) == "MCD"

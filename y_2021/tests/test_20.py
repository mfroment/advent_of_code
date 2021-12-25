from y_2021.d_20 import *

input_values, enhance = parse_input(__file__)


def test_1():
    assert solve(input_values, enhance, 2) == 35


def test_2():
    assert solve(input_values, enhance, 50) == 3351

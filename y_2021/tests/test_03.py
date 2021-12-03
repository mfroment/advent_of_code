from y_2021.d_03 import *

input_bitarrays = parse_input(__file__)


def test_1():
    assert solve_1(input_bitarrays) == 198


def test_2():
    assert solve_2(input_bitarrays) == 230

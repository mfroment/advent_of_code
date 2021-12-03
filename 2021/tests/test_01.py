from d_01 import *

input_depths = parse_input(__file__)


def test_1():
    assert solve(input_depths, 1) == 7


def test_2():
    assert solve(input_depths, 3) == 5

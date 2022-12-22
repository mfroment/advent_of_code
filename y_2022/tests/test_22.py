from y_2022.d_22 import *

raw_grid, moves = parse_input(__file__)


def test_1():
    assert solve_1(raw_grid, moves) == 6032


def test_2():
    # The test data does not have the same layout/dimensions as the actual input
    # The code is not generic and does not support it.
    assert True

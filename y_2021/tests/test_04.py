from y_2021.d_04 import *

input_drawings, input_grids = parse_input(__file__)


def test_1():
    assert solve_1(input_drawings, input_grids) == 4512


def test_2():
    assert solve_2(input_drawings, input_grids) == 1924

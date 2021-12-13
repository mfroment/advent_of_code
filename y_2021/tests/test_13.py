from y_2021.d_13 import *

input_dots, input_folds = parse_input(__file__)


def test_1():
    assert solve_1(input_dots, input_folds) == 17


def test_2():
    assert solve_2(input_dots, input_folds) == {(0, 1), (4, 4), (2, 4), (4, 0), (0, 4), (3, 4), (4, 3), (0, 0), (0, 3),
                                                (2, 0), (4, 2), (1, 4), (3, 0), (0, 2), (1, 0), (4, 1)}

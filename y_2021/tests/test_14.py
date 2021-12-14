from y_2021.d_14 import *

input_polypairs, input_insertions = parse_input(__file__)


def test_1():
    assert solve_1(input_polypairs, input_insertions) == 1588


def test_2():
    assert solve_2(input_polypairs, input_insertions) == 2188189693529

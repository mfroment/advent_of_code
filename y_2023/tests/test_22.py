import aoc.utils as aocu
from y_2023.d_22 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == aocu.s2i("5")


def test_2():
    assert solve_2(input_values) == aocu.s2i("7")

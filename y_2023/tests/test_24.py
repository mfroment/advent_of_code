import aoc.utils as aocu
from y_2023.d_24 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values, 7, 27) == aocu.s2i("2")


def test_2():
    assert solve_2(input_values) == aocu.s2i("47")

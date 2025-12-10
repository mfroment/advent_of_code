from y_2023.d_11 import *
import aoc.utils as aocu

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == aocu.s2i("374")


def test_2():
    assert solve(input_values, 10) == aocu.s2i("1030")
    assert solve(input_values, 100) == aocu.s2i("8410")

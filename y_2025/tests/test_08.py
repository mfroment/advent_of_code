from y_2025.d_08 import *
import aoc.utils as aocu

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values, 10) == aocu.s2i("40")


def test_2():
    assert solve_2(input_values) == aocu.s2i("25272")

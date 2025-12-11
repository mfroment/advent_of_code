from y_2025.d_11 import *
import aoc.utils as aocu


def test_1():
    input_values = parse_input(__file__, "1")
    assert solve_1(input_values) == aocu.s2i("5")


def test_2():
    input_values = parse_input(__file__, "2")
    assert solve_2(input_values) == aocu.s2i("2")

from y_2023.d_01 import *
import aoc.utils as aocu


def test_1():
    input_values = parse_input(__file__, suffix="1")
    assert solve_1(input_values) == aocu.s2i("142")


def test_2():
    input_values = parse_input(__file__, suffix="2")
    assert solve_2(input_values) == aocu.s2i("281")

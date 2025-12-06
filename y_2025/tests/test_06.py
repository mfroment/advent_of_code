from y_2025.d_06 import *
import aoc.utils as aocu


def test_1():
    input_values = parse_input_1(__file__)
    assert solve(input_values) == aocu.s2i('4277556')


def test_2():
    input_values = parse_input_2(__file__)
    assert solve(input_values) == aocu.s2i('3263827')

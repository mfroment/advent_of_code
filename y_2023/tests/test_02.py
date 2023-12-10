from y_2023.d_02 import *
import aoc.utils as aocu

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == aocu.s2i('8')


def test_2():
    assert solve_2(input_values) == aocu.s2i('2286')

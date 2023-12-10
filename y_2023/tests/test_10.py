from y_2023.d_10 import *
import aoc.utils as aocu


def test_1():
    input_values = parse_input(__file__, suffix='1a')
    assert solve_1(input_values) == aocu.s2i('4')

    input_values = parse_input(__file__, suffix='1b')
    assert solve_1(input_values) == aocu.s2i('4')

    input_values = parse_input(__file__, suffix='1c')
    assert solve_1(input_values) == aocu.s2i('8')

    input_values = parse_input(__file__, suffix='1d')
    assert solve_1(input_values) == aocu.s2i('8')


def test_2():
    input_values = parse_input(__file__, suffix='2a')
    assert solve_2(input_values) == aocu.s2i('4')

    input_values = parse_input(__file__, suffix='2b')
    assert solve_2(input_values) == aocu.s2i('8')

    input_values = parse_input(__file__, suffix='2c')
    assert solve_2(input_values) == aocu.s2i('10')

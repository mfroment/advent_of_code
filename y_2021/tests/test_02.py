from y_2021.d_02 import *

input_commands = parse_input(__file__)


def test_1():
    assert solve_1(input_commands) == 150


def test_2():
    assert solve_2(input_commands) == 900

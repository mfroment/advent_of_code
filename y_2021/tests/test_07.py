from y_2021.d_07 import *

input_values = parse_input(__file__)


def test_1():
    assert solve_naive(input_values, fuel_consumption_1) == 37


def test_2():
    assert solve_naive(input_values, fuel_consumption_2) == 168

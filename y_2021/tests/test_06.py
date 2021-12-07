from y_2021.d_06 import *

input_fishes = parse_input(__file__)


def test_1():
    assert solve(input_fishes, 80) == 5934


def test_2():
    assert solve(input_fishes, 256) == 26984457539

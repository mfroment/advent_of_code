from y_2021.d_18 import *

input_values = parse_input(__file__)


def test_1():
    for v in input_values:
        print(v)
        # print(l2s(v))
        # print(s2l(l2s(v)))
        # print(s2l(process(l2s(v))))
    assert solve_1(input_values) == None


def test_2():
    assert solve_2(input_values) == None

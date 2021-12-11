from y_2020.d_25 import *

input_pkeys = parse_input(__file__)


def test_1():
    assert modular_log(GENERATOR, input_pkeys[0], MODULUS) == 8
    assert modular_log(GENERATOR, input_pkeys[1], MODULUS) == 11
    assert solve_1(input_pkeys) == 14897079


def test_2():
    assert solve_2(input_pkeys) == None

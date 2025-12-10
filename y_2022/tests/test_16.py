from y_2022.d_16 import *

tunnels, flows = parse_input(__file__)


def test_1():
    assert solve_1(tunnels, flows) == 1651


def test_2():
    assert solve_2(tunnels, flows) == 1707

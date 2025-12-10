from y_2021.d_15 import *

input_values = parse_input(__file__)
output_nuply = parse_input(__file__, "nuply_output")


def test_1():
    assert Sweep.solve_1(input_values) == 40  # only working because trivial case with no no up / left moves
    assert Clunky.solve_1(input_values) == 40
    assert Cleaner.solve_1(input_values) == 40


def test_2():
    assert nuply(input_values, 5) == output_nuply
    assert Sweep.solve_2(input_values) == 315  # only working because trivial case with no no up / left moves
    assert Clunky.solve_2(input_values) == 315
    assert Cleaner.solve_2(input_values) == 315

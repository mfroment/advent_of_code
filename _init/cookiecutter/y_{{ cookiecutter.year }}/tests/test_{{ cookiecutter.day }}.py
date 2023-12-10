from y_{{ cookiecutter.year }}.d_{{ cookiecutter.day }} import *
import aoc.utils as aocu

input_values = parse_input(__file__)


def test_1():
    assert solve_1(input_values) == aocu.s2i('{{ cookiecutter.example_answer_a }}')


def test_2():
    assert solve_2(input_values) == aocu.s2i('{{ cookiecutter.example_answer_b }}')

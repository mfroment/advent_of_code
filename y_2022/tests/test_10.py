from y_2022.d_10 import *

input_values = parse_input(__file__)

x, screen = process(input_values)


def test_1():
    assert solve_1(x) == 13140


def test_2():
    expected = """
██  ██  ██  ██  ██  ██  ██  ██  ██  ██  
███   ███   ███   ███   ███   ███   ███ 
████    ████    ████    ████    ████    
█████     █████     █████     █████     
██████      ██████      ██████      ████
███████       ███████       ███████     """
    assert solve_2(screen) == expected

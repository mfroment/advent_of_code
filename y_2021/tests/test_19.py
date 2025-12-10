from y_2021.d_19 import *

input_scanners = parse_input(__file__)

all_beacons = solve(input_scanners)


def test_1():
    assert len(all_beacons) == 79


def test_2():
    assert largest_manhattan_distance(input_scanners) == 3621

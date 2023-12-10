import time
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    res = []
    for c in aocu.reduce_input(aocu.read_input(file, suffix)):
        if c == '>':
            res.append((1, 0))
        else:
            res.append((-1, 0))
    return res


class Chamber:
    def __init__(self):
        self.height = 0
        self.rocks = set()

    def add_shape(self, shape):
        self.rocks |= set(shape.pos)
        self.height = max(self.height, max(y for (_, y) in shape.pos))

    def is_colliding(self, pos):
        return any(p in self.rocks for p in pos) or any(x == 0 or x == 8 or y == 0 for (x, y) in pos)

    def __str__(self):
        col = [[c for c in '|.......|'] for _ in range(self.height + 1)]
        for x, y in self.rocks:
            col[y][x] = '#'
        return '\n' + '\n'.join(''.join(c) for c in reversed(col))


class ShapedRock:
    SHAPES = (
        ((3, 4), (4, 4), (5, 4), (6, 4)),
        ((4, 4), (3, 5), (4, 5), (5, 5), (4, 6)),
        ((3, 4), (4, 4), (5, 4), (5, 5), (5, 6)),
        ((3, 4), (3, 5), (3, 6), (3, 7)),
        ((3, 4), (4, 4), (3, 5), (4, 5))
    )

    def __init__(self, shape_index, height):
        assert 0 <= shape_index < len(ShapedRock.SHAPES)
        self.shape_index = shape_index
        self.pos = tuple((x, y + height) for (x, y) in ShapedRock.SHAPES[shape_index])

    def shifted_pos(self, shift):
        dx, dy = shift
        s_pos = tuple((x + dx, y + dy) for (x, y) in self.pos)
        return s_pos

    def update_pos(self, pos):
        self.pos = pos


def compute_fall(pti, chamber, lateral_shifts, cursor):
    shaped_rock = ShapedRock(pti, chamber.height)
    while True:
        pos = shaped_rock.shifted_pos(lateral_shifts[cursor])
        if not chamber.is_colliding(pos):
            shaped_rock.update_pos(pos)
        cursor = (cursor + 1) % len(lateral_shifts)
        pos = shaped_rock.shifted_pos((0, -1))
        if chamber.is_colliding(pos):
            chamber.add_shape(shaped_rock)
            return cursor, shaped_rock
        shaped_rock.update_pos(pos)


def solve_1(values):
    chamber = Chamber()
    cursor = 0
    for i in range(2022):
        cursor, _ = compute_fall(i % 5, chamber, values, cursor)
    return chamber.height


def solve_2(values):
    total_i = 1000000000000
    # First run until detection of a cycle i.e. the current value of (shape #1's left x-position, cursor)
    # has been seen before. (note: this is a leap of faith and not 100% robust, there are situations
    # where this test won't work, i.e. if next pieces fall below said shaped #1 or not)
    #   tracked_i: iteration at which the cycle began
    #   tracked_h: height when the cycle began
    #   delta_i: number of iterations in the cycle
    #   delta_h: height added during the cycle
    tracked_i, tracked_h, delta_i, delta_h = None, None, None, None
    chamber = Chamber()
    cursor = 0
    tracker = dict()
    for i in range(total_i):
        previous_height = chamber.height
        cursor, shape = compute_fall(i % 5, chamber, values, cursor)
        left_x = shape.pos[0][0]
        if i % 5 == 0:
            k = (cursor, left_x)
            if k in tracker:  # cycle detected... probably
                tracked_i, tracked_h = tracker[k]
                delta_i, delta_h = i - tracked_i, previous_height - tracked_h
                break
            else:
                tracker[k] = (i, previous_height)
    # Compute the height added by cycles:
    cycles_h = ((total_i - tracked_i) // delta_i) * delta_h
    # Now run a simulation with the cycles "removed" i.e. run the first tracked_i iterations
    # before the cycles begin, and the last remaining_i iterations after the last complete
    # cycle has ended.
    remaining_i = (total_i - tracked_i) % delta_i
    rerun_i = tracked_i + remaining_i
    chamber = Chamber()
    cursor = 0
    for i in range(rerun_i):
        cursor, _ = compute_fall(i % 5, chamber, values, cursor)
    return chamber.height + cycles_h


if __name__ == "__main__":
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")

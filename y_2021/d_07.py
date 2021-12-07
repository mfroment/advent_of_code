from pathlib import Path
import statistics


def parse_input(file=__file__):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem)) as f:
        return [int(r) for r in f.readline().split(',')]


def fuel_consumption_1(values, target):
    res = 0
    for v in values:
        res += abs(v - target)
    return res


def fuel_consumption_2(values, target):
    res = 0
    for v in values:
        res += abs(v - target) * (abs(v - target) + 1) // 2
    return res


def solve_naive(values, fuel_consumption):
    # Scan every candidate value. Very inefficient, but good enough for the size of the input
    min_fuel = None
    for target in range(min(values), max(values) + 1):
        fuel = fuel_consumption(values, target)
        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
    return min_fuel

# Don't bother with improving the search method for the global minimum of a convex fuction, there is better:

def solve_1(values):
    # The optimal position is the median (for odd number of inputs; the median range for even number of inputs)
    return fuel_consumption_1(values, int(statistics.median(values)))


def solve_2(values):
    # The optimal position is the mean m (if it's an integer; if not, it's either int(m), int(m)+1)
    # Consider the incremental fuel consumption:
    #    f(x)   == sum([(x-v)  *(x-v+1)//2 for v in values]
    #    f(x-1) == sum([(x-v-1)*(x-v)  //2 for v in values]
    #    f(x)-f(x-1) == sum([(x-v)*(x-v+1-x+v+1) // 2 for v in values]
    #                == sum([2*(x-v) // 2 for v in values ]
    #                == sum([x-v for v in values])
    #                == n*x - sum(values)
    #    This is negative is x<mean(values) and positive if x>mean(values).
    #    In other words, the fuel consumption is decreasing until x reaches the mean value, then increases.
    #    Therefore, the minimum fuel consumption is reached at the mean (rounded up or down if not an integer).
    avg = int(statistics.mean(values))
    return min([fuel_consumption_2(values, m) for m in [avg, avg + 1]])


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_naive(input_values, fuel_consumption_1), solve_1(input_values))
    print("Part 2:", solve_naive(input_values, fuel_consumption_2), solve_2(input_values))

    input_values = [1,5000,5000]
    print("Part 2:", solve_naive(input_values, fuel_consumption_2), solve_2(input_values))

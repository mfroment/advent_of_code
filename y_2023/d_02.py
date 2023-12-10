import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    values = {}
    for section in sections[0]:
        game_id = int(re.sub(r"^Game (\d+):.*$", r"\1", section))
        values[game_id] = []
        game_def = re.sub(r"^Game \d+: (.*)$", r"\1", section)
        game_trials = game_def.split("; ")
        for game_trial in game_trials:
            draws = {}
            for s in game_trial.split(", "):
                v, color = s.split(" ")
                draws[color] = int(v)
            values[game_id].append(draws)

    return values


def solve_1(values):
    res = 0
    for game_id, game_trials in values.items():
        if all([game_det.get("red",0) <=12 
                and game_det.get("green",0) <=13 
                and game_det.get("blue",0) <= 14
                for game_det in game_trials]):
            res += game_id
    return res


def solve_2(values):
    res = 0
    for game_trials in values.values():
        r, g, b = 0, 0, 0
        for game_det in game_trials:
            r = max(game_det.get("red",0), r)
            g = max(game_det.get("green",0), g)
            b = max(game_det.get("blue",0), b)
        p = r * g * b
        res += p
    return res



def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

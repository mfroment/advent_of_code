from itertools import product
from collections import Counter


def roll_one_100_dice():
    roll_one_100_dice.res = getattr(roll_one_100_dice, "res", 0) % 100 + 1
    return roll_one_100_dice.res


def solve_1(p1, p2):
    roll_count = 0
    pos = [p1, p2]
    scores = [0, 0]
    player = 0
    playing = True
    while playing:
        roll_count += 3
        mov = sum(roll_one_100_dice() for _ in range(3))
        pos[player] = ((pos[player] - 1 + mov) % 10) + 1
        scores[player] += pos[player]
        playing = scores[player] < 1000
        player = 1 - player  # switch player before testing score, so we'll get the loser's score
    return roll_count * scores[player]


def roll_three_dirac_dices():
    # Pseudo constant (compute only once)
    return getattr(
        roll_three_dirac_dices,
        "res",
        Counter(d1 + d2 + d3 for d1, d2, d3 in product((1, 2, 3), (1, 2, 3), (1, 2, 3))),
    )


def play_quantum_game(pos, score=0, depth=0):
    if score >= 21:
        return {depth: 1}, {}  # this universe is a winning universe, no more universe spawn
    else:
        wins = dict()
        notwins = {depth: 1}  # at this depth, this universe is not a winning universe
        # spawn the children universes:
        for mv, factor in roll_three_dirac_dices().items():
            npos = ((pos - 1 + mv) % 10) + 1
            nscore = score + npos
            rn, rnl = play_quantum_game(npos, nscore, depth + 1)
            for k in rn:
                wins[k] = wins.get(k, 0) + rn[k] * factor
            for k in rnl:
                notwins[k] = notwins.get(k, 0) + rnl[k] * factor
        return wins, notwins


def solve_2(a, b):
    wins1, notwins1 = play_quantum_game(a)
    wins2, notwins2 = play_quantum_game(b)
    winner1 = 0
    for k1, c1 in wins1.items():
        winner1 += c1 * notwins2.get(k1 - 1, 0)
    winner2 = 0
    for k2, c2 in wins2.items():
        winner2 += c2 * notwins1.get(k2, 0)
    return max(winner1, winner2)


if __name__ == "__main__":
    print("Part 1:", solve_1(4, 9))
    print("Part 2:", solve_2(4, 9))

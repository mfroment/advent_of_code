import time
import re
import aoc.utils as aocu

from functools import cmp_to_key
from collections import Counter


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            cards, bet = re.split(r",|-|\s+", line, maxsplit=0)
            sub_res.append((cards, int(bet)))
        res.append(sub_res)
    return aocu.reduce_input(res)  # dimensionality reduction


def cmp_cards(a, b, card_values):
    assert len(a) == len(b)
    for ca, cb in zip(a, b):
        if ca != cb:
            return card_values.index(ca) - card_values.index(cb)
    return 0


HAND_TYPES = ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1))


def get_hand_type(cards, has_joker=False):
    card_counts = Counter(cards)
    if not has_joker:
        hand_type = tuple(sorted(card_counts.values(), reverse=True))
    else:
        if "J" in card_counts and len(card_counts) > 1:
            # J is a joker and there are other cards; bonus count for the most common card
            bonus = card_counts["J"]
            del card_counts["J"]
        else:
            # either no J or J is the only card; no bonus count
            bonus = 0
        hand_type = list(sorted(card_counts.values(), reverse=True))
        hand_type[0] += bonus
        hand_type = tuple(hand_type)
    return hand_type


def cmp_hand_type(a, b):
    return HAND_TYPES.index(a) - HAND_TYPES.index(b)


def cmp_hand(a, b, card_value_order, has_joker=False):
    assert len(a) == len(b)
    return cmp_hand_type(get_hand_type(a, has_joker), get_hand_type(b, has_joker)) or cmp_cards(a, b, card_value_order)


def solve(values, cmp_hand_func):
    sorted_hands = sorted(values, key=cmp_to_key(cmp_hand_func), reverse=True)
    score = 0
    for i, hand in enumerate(sorted_hands):
        score += (i + 1) * hand[1]
    return score


def solve_1(values):
    return solve(values, lambda a, b: cmp_hand(a[0], b[0], "AKQJT98765432"))


def solve_2(values):
    return solve(values, lambda a, b: cmp_hand(a[0], b[0], "AKQT98765432J", has_joker=True))


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

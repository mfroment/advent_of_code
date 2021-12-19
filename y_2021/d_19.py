from pathlib import Path
import numpy as np
import re
import ast
from itertools import combinations

VERBOSE = True
MATCH_COUNT = 12


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    scanners = dict()
    scanner_id = None
    beacons = None
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        for r in f.readlines() + ['']:
            r = r.strip()
            if r == '':
                if scanner_id is not None:
                    scanners[scanner_id] = Scanner(None, None, np.asarray(beacons))
                scanner_id = None
            else:
                m = re.search(r'^--- scanner (\d+) ---$', r)
                if m:
                    scanner_id = int(m.group(1))
                    beacons = []
                else:  # must be coordinates
                    beacons.append(ast.literal_eval('[' + r + ']'))
    return scanners


# Scanner
class Scanner:
    def __init__(self, pos, rot, beacons):
        self.pos = pos
        self.rot = rot
        self.beacons = beacons

    def update(self, pos, rot, beacons=None):
        # Update position, rotation, coordinates of beacons in the base frame
        self.pos = pos
        self.rot = rot
        if beacons is None:
            self.beacons = np.asarray(-pos + self.beacons * rot)
        else:
            self.beacons = beacons


# Rotations
class Rotations:
    """ The 24 distinct 90-degree based rotations in 3D space """
    _rots = None

    @classmethod
    def get(cls):
        if cls._rots is None:
            cls._rots = []
            rz = np.matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
            rx = np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
            ry = np.matrix([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        r = (np.linalg.matrix_power(rx, i) * np.linalg.matrix_power(ry, j) *
                             np.linalg.matrix_power(rz, k)).astype(int)
                        if not any(np.array_equal(re, r) for re in cls._rots):
                            cls._rots.append(r)
        return cls._rots

    @classmethod
    def identity(cls):
        return cls.get()[0]


# Solving = Find position & rotation of all scanners, and aggregate unique beacons.
def solve(scanners):
    # Initialize with scanner 0 defining the absolute reference frame & first "source" to match "targets" with:
    scanners[0].update(np.array([0, 0, 0]), Rotations.identity())
    all_beacons = setify_list_of_arrays(scanners[0].beacons)
    sources = {0}
    targets = set(scanners.keys()) - {0}
    while len(targets) > 0:
        # Sanity check: there must be sources scanners left to determine the position of targets scanners
        assert len(sources) > 0
        # Select a remaining source (and remove it, it will be used only once)
        src_id = sources.pop()
        if VERBOSE: print('source:', src_id)
        matched = set()
        for tgt_id in targets:
            if VERBOSE: print('  target:', tgt_id)
            # Try to match scanners #src_id and #tgt_id
            # If a match is found, add tgt_id to sources,
            # and update its position/rotation/beacons in the scanners[0]'s reference frame
            if match_and_update(scanners[src_id], scanners[tgt_id]):
                # scanners[tgt_id].update(pos, rot, all_beacons)
                matched.add(tgt_id)
                all_beacons |= setify_list_of_arrays(scanners[tgt_id].beacons)
                if VERBOSE: print('        matched!', len(all_beacons))
                if VERBOSE: print('    pos', scanners[tgt_id].pos)
        # Matched targets are removed from targets and added to sources
        targets -= matched
        sources.update(matched)
    return all_beacons


def setify_list_of_arrays(loa):
    return {tuple(x for x in arr) for arr in loa}


def match_and_update(src, tgt):
    src_beacons_set = setify_list_of_arrays(src.beacons)
    for rot in Rotations.get():  # Apply all rotations to the tgt reference frame until match (or exhaustion)
        tgt_rot_beacons = np.asarray(tgt.beacons * rot)
        # Pair (almost) all beacons from src & tgt, and check if the resulting [tgt -> src] translation applied to other
        # tgt beacons result into at least a group of MATCH_COUNT matches. If yes, we have a scanner match.
        # When checking translations, we don't need to loop on the last MATCH_COUNT-1 src beacons (because a translation
        # leading to a scanner match would also include one of the prior src beacons; and they have already been tried).
        for src_b in src.beacons[:len(src.beacons) - MATCH_COUNT + 1]:
            for tgt_b in tgt_rot_beacons:
                pos = tgt_b - src_b  # -translation = relative position of tgt scanner in src scanner reference frame
                tgt_pos_rot_beacons = np.asarray(-pos + tgt_rot_beacons)
                inter = src_beacons_set & setify_list_of_arrays(tgt_pos_rot_beacons)
                if len(inter) >= MATCH_COUNT:
                    tgt.update(pos, rot, tgt_pos_rot_beacons)
                    return True
    return False


def manhattan_distance(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def largest_manhattan_distance(scanners):
    return max({manhattan_distance(scanners[k1].pos, scanners[k2].pos) for k1, k2 in combinations(scanners.keys(), 2)})


if __name__ == "__main__":
    input_scanners = parse_input()

    all_beacons = solve(input_scanners)

    print("Part 1:", len(all_beacons))
    print("Part 2:", largest_manhattan_distance(input_scanners))

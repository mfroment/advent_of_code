import time
import re
import aoc.utils as aocu


def parse_input(file=__file__, suffix=None):
    sections = aocu.read_input(file, suffix)
    res = []
    for section in sections:
        sub_res = []
        for line in section:
            tokens = re.split(r",|-|\s+", line, maxsplit=0)
            tokens = [aocu.s2i(t) for t in tokens]
            sub_res.append(tokens)
        res.append(sub_res)
    seeds = res[0][0][1:]
    maps = [r[1:] for r in res[1:]]
    return seeds, maps


def solve_1(values):
    def remap(value, map):
        for dest, src, ln in map:
            if src <= value < src + ln:
                return dest + value - src
        return value

    def remap_along_sequence_of_maps(value, maps):
        for map in maps:
            value = remap(value, map)
        return value

    seeds, maps = values
    return min(remap_along_sequence_of_maps(seed, maps) for seed in seeds)


def solve_2(values):
    def remap_range_along_maplet(rnge, maplet):
        # a range is a tuple (start, length), a maplet is a tuple (dest, src, length)
        rnge_start, rnge_ln = rnge
        dest, src, ln = maplet
        # unremapped range on the left of the mapping interval
        r_l = (rnge_start, min(src - rnge_start, rnge_ln))
        if r_l[1] <= 0:
            r_l = None
        # remapped middle interval intersecting the mapping interval
        r_m = (
            max(src, rnge_start),
            min(rnge_start + rnge_ln, src + ln) - max(src, rnge_start),
        )
        if r_m[1] <= 0:
            r_m = None
        else:
            r_m = (dest + r_m[0] - src, r_m[1])
        # unremapped range on the right of the mapping interval
        r_r = (
            max(src + ln, rnge_start),
            rnge_start + rnge_ln - max(src + ln, rnge_start),
        )
        if r_r[1] <= 0:
            r_r = None
        # return [unremapped intervals], [remapped interval]  -- they can be empty lists
        return [r for r in [r_l, r_r] if r is not None], [] if r_m is None else [r_m]

    def remap_ranges_along_map(rnges, map):
        # we do the same as above for all ranges, applying the map maplet by maplet
        # the remapped ranges are stored aside on each step, and the yet unremapped ones are passed to the next step
        unremappeds = rnges
        remappeds = []
        for maplet in map:
            next_unremappeds = []
            for unremapped in unremappeds:
                new_unremappeds, new_remappeds = remap_range_along_maplet(unremapped, maplet)
                next_unremappeds += new_unremappeds
                remappeds += new_remappeds
            unremappeds = next_unremappeds
        return unremappeds + remappeds

    def remap_ranges_along_sequence_of_maps(rnges, maps):
        res = rnges
        for map in maps:
            res = remap_ranges_along_map(res, map)
        return res

    # prepare the ranges, and the sequence of maps
    seeds, maps = values
    rnges = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    res = remap_ranges_along_sequence_of_maps(rnges, maps)
    # return the minimum of the left bounds of the ranges - that's the answer
    return min(r[0] for r in res)


def main():
    input_values = parse_input()

    start_time = time.time()
    print(f"Part 1: {str(solve_1(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")
    start_time = time.time()
    print(f"Part 2: {str(solve_2(input_values)):<30}{'(':>30}{time.time() - start_time:.3f}s)")


if __name__ == "__main__":
    main()

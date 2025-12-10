from pathlib import Path


def read_input(file, suffix=None):
    p = Path(file)
    sections = []
    section = []
    with open(p.parent.joinpath("input").joinpath(p.stem + ("" if suffix is None else "-" + suffix) + ".txt")) as f:
        for line in f.read().splitlines():
            if line == "":
                if len(section) > 0:
                    sections.append(section)
                    section = []
                continue
            section.append(line)
        if len(section) > 0:
            sections.append(section)
    return sections


def reduce_input(lolol):
    # Assuming sections of lines of tokens i.e. list of list of list, none empty
    # d3
    maxlen = 0
    for lol in lolol:
        for l in lol:
            maxlen = max(maxlen, len(l))
    if maxlen == 1:
        for i, lol in enumerate(lolol):
            lolol[i] = [l[0] for l in lol]
    # d2
    maxlen = 0
    for lol in lolol:
        maxlen = max(maxlen, len(lol))
    if maxlen == 1:
        lolol = [lol[0] for lol in lolol]
    # d1
    if len(lolol) == 1:
        lolol = lolol[0]
    return lolol

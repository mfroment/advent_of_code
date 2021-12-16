from pathlib import Path
from numpy import prod


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        s = f.readline().strip()
        return s


def bitify(s):
    return bin(int(s, 16))[2:].zfill(len(s) * 4)


def decode(bs):
    if bs == '' or int(bs, 2) == 0:
        return []
    ver = int(bs[:3], 2)
    typ = int(bs[3:6], 2)
    if typ == 4:
        v, u, rbs = decode_lit(bs[6:])
    elif bs[6] == '0':
        v, u, rbs = decode_op0(bs[7:])
    else:
        v, u, rbs = decode_op1(bs[7:])
    return [(ver, typ, v)] + u + decode(rbs)


def decode_op0(bs):
    leng = int(bs[:15], 2)
    sub_bs = bs[15:15 + leng]
    rbs = bs[15 + leng:]
    return decode(sub_bs), [], rbs


def decode_op1(bs):
    count = int(bs[:11], 2)
    rbs = bs[11:]
    res = decode(rbs)
    return res[:count], res[count:], ''


def decode_lit(bs):
    rbs = bs
    vs = ''
    cont = True
    while cont:
        cont = (rbs[0] == '1')
        vs += rbs[1:5]
        rbs = rbs[5:]
    v = int(vs, 2)
    return v, [], rbs


def packet_list_version(pl):
    return sum(packet_version(p) for p in pl)


def packet_version(p):
    return p[0] + (0 if isinstance(p[2], int) else packet_list_version(p[2]))


def packet_list_values(pl):
    return [packet_value(p) for p in pl]


def packet_value(p):
    t, v = p[1], p[2]
    if t == 4:
        return v
    plv = packet_list_values(v)
    if t == 0:
        return sum(plv)
    elif t == 1:
        return prod(plv)
    elif t == 2:
        return min(plv)
    elif t == 3:
        return max(plv)
    else:
        assert len(plv) == 2 and t in {5, 6, 7}
        a, b = plv
        if t == 5:
            return 1 if a > b else 0
        elif t == 6:
            return 1 if a < b else 0
        elif t == 7:
            return 1 if a == b else 0


def solve_1(values):
    return packet_list_version(decode(bitify(values)))


def solve_2(values):
    return packet_list_values(decode(bitify(values)))[0]


if __name__ == "__main__":
    input_values = parse_input()

    print("Part 1:", solve_1(input_values))
    print("Part 2:", solve_2(input_values))

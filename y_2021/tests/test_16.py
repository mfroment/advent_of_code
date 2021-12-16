from y_2021.d_16 import *


def test_0():
    test_data = {
        'D2FE28': ('110100101111111000101000', [(6, 4, 2021)]),
        '38006F45291200': (
        '00111000000000000110111101000101001010010001001000000000', [(1, 6, [(6, 4, 10), (2, 4, 20)])]),
        'EE00D40C823060': (
        '11101110000000001101010000001100100000100011000001100000', [(7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)])]),
    }
    for inp, (outpb, outpp) in test_data.items():
        assert bitify(inp) == outpb
        assert decode(outpb) == outpp


def test_1():
    test_data = {
        '8A004A801A8002F478': 16,
        '620080001611562C8802118E34': 12,
        'C0015000016115A2E0802F182340': 23,
        'A0016C880162017C3686B18A3D4780': 31,
    }
    for inp, outp in test_data.items():
        assert solve_1(inp) == outp


def test_2():
    test_data = {
        'C200B40A82': 3,
        '04005AC33890': 54,
        '880086C3E88112': 7,
        'CE00C43D881120': 9,
        'D8005AC2A8F0': 1,
        'F600BC2D8F': 0,
        '9C005AC2F8F0': 0,
        '9C0141080250320F1802104A08': 1,
    }
    for inp, outp in test_data.items():
        assert solve_2(inp) == outp

#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple


def binary(data: str) -> str:
    result = ''

    for symbol in data:
        result += format(int(symbol, 16), "04b")

    return result


def read_packets(data: str, index: int) -> Tuple[List[Dict[str, int]], int]:
    packet = {
        "version": int(data[index: index + 3], 2),
        "type_id": int(data[index + 3: index + 6], 2)
    }

    index = index + 6

    if packet["type_id"] == 4:
        literal = ''

        while data[index] != '0':
            literal += data[index + 1: index + 5]
            index += 5

        literal += data[index + 1: index + 5]
        packet['literal'] = int(literal, 2)
        index += 5
        packets = [packet]
    else:
        length_type_id = data[index]

        if length_type_id == '0':
            packets = [packet]
            sub_bits = int(data[index + 1: index + 16], 2)
            index += 16
            end = index + sub_bits
            while index < end:
                subpackets, index = read_packets(data, index)
                packets.extend(subpackets)
        else:
            packets = [packet]
            sub_cnt = int(data[index + 1: index + 12], 2)
            index = index + 12
            for i in range(sub_cnt):
                subpackets, index = read_packets(data, index)
                packets.extend(subpackets)

    return packets, index


def decode_packets(data: str) -> int:

    data = binary(data)
    index = 0
    result = 0

    while index < len(data) and '1' in data[index:]:
        packets, index = read_packets(data, index)
        for packet in packets:
            result += packet['version']

    return result


class TestClass():

    def test_1(self):
        data = '8A004A801A8002F478'
        assert decode_packets(data) == 16

        data = '620080001611562C8802118E34'
        assert decode_packets(data) == 12

        data = 'C0015000016115A2E0802F182340'
        assert decode_packets(data) == 23

        data = 'A0016C880162017C3686B18A3D4780'
        assert decode_packets(data) == 31


def main():
    data = next(sys.stdin).strip()
    result = decode_packets(data)
    print(result)


if __name__ == '__main__':
    main()

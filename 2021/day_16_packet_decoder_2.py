#!/usr/bin/env python3

import sys
from typing import Dict, Tuple


def binary(data: str) -> str:
    result = ''

    for symbol in data:
        result += format(int(symbol, 16), "04b")

    return result


def read_packet(data: str, index: int) -> Tuple[Dict[str, int], int]:
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
    else:
        packets = []
        length_type_id = data[index]

        if length_type_id == '0':
            sub_bits = int(data[index + 1: index + 16], 2)
            index += 16
            end = index + sub_bits
            while index < end:
                subpacket, index = read_packet(data, index)
                packets.append(subpacket)
        else:
            sub_cnt = int(data[index + 1: index + 12], 2)
            index = index + 12
            for i in range(sub_cnt):
                subpacket, index = read_packet(data, index)
                packets.append(subpacket)

        if packet["type_id"] == 0:
            packet["literal"] = sum(
                [subpacket["literal"] for subpacket in packets])
        elif packet["type_id"] == 1:
            packet["literal"] = 1
            for subpacket in packets:
                packet["literal"] *= subpacket["literal"]
        elif packet["type_id"] == 2:
            packet["literal"] = min(
                [subpacket["literal"] for subpacket in packets])
        elif packet["type_id"] == 3:
            packet["literal"] = max(
                [subpacket["literal"] for subpacket in packets])
        elif packet["type_id"] == 5:
            packet["literal"] = (
                1 if packets[0]["literal"] > packets[1]["literal"]
                else 0
            )
        elif packet["type_id"] == 6:
            packet["literal"] = (
                1 if packets[0]["literal"] < packets[1]["literal"]
                else 0
            )
        elif packet["type_id"] == 7:
            packet["literal"] = (
                1 if packets[0]["literal"] == packets[1]["literal"]
                else 0
            )

    return packet, index


def decode_packets(data: str) -> int:
    data = binary(data)
    packet, index = read_packet(data, 0)
    return packet['literal']


class TestClass():

    def test_1(self):
        data = 'C200B40A82'
        assert decode_packets(data) == 3

        data = '04005AC33890'
        assert decode_packets(data) == 54

        data = '880086C3E88112'
        assert decode_packets(data) == 7

        data = 'CE00C43D881120'
        assert decode_packets(data) == 9

        data = 'D8005AC2A8F0'
        assert decode_packets(data) == 1

        data = 'F600BC2D8F'
        assert decode_packets(data) == 0

        data = '9C005AC2F8F0'
        assert decode_packets(data) == 0

        data = '9C0141080250320F1802104A08'
        assert decode_packets(data) == 1


def main():
    data = next(sys.stdin).strip()
    result = decode_packets(data)
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
from typing import List


def most_common(data: List[str], bit_pos: int, default: str = '1') -> str:
    cnt = 0

    for item in data:
        if item[bit_pos] == '1':
            cnt += 1

    if cnt == len(data) - cnt:
        return default

    if cnt > len(data) - cnt:
        return '1'

    return '0'


def life_support_rating(data: List[str]) -> int:
    candidates_1, candidates_2 = [], []
    common_bit = most_common(data, 0)

    for line in data:
        if line[0] == common_bit:
            candidates_1.append(line)
        else:
            candidates_2.append(line)

    bit_pos = 1

    while len(candidates_1) > 1:
        common_bit = most_common(candidates_1, bit_pos)
        candidates_1 = [x for x in candidates_1 if x[bit_pos] == common_bit]
        bit_pos += 1

    bit_pos = 1

    while len(candidates_2) > 1:
        common_bit = most_common(candidates_2, bit_pos)
        candidates_2 = [x for x in candidates_2 if x[bit_pos] != common_bit]
        bit_pos += 1

    return int(candidates_1[0], 2) * int(candidates_2[0], 2)


class TestClass():

    def test_1(self):
        data = [
            '00100',
            '11110',
            '10110',
            '10111',
            '10101',
            '01111',
            '00111',
            '11100',
            '10000',
            '11001',
            '00010',
            '01010',
        ]

        assert life_support_rating(data) == 230


def main():
    data = [x.strip() for x in sys.stdin]
    result = life_support_rating(data)
    print(result)


if __name__ == '__main__':
    main()

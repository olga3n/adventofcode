#!/usr/bin/env python3

import sys
from typing import Iterable


def power_consumption(data: Iterable[str]) -> int:
    size = 0
    n_size = 0
    vector = []

    for ind, line in enumerate(data):
        if ind == 0:
            n_size = len(line)
            vector = [0] * n_size

        for ind in range(n_size):
            if line[ind] == '1':
                vector[ind] += 1

        size += 1

    value_1, value_2 = '', ''

    for ind in range(n_size):
        if vector[ind] > size - vector[ind]:
            value_1 += '1'
            value_2 += '0'
        else:
            value_1 += '0'
            value_2 += '1'

    return int(value_1, 2) * int(value_2, 2)


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

        assert power_consumption(data) == 198


def main():
    data = map(lambda x: x.strip(), sys.stdin)
    result = power_consumption(data)
    print(result)


if __name__ == '__main__':
    main()

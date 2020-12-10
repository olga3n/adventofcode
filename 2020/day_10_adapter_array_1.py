#!/usr/bin/env python3

import sys


def adapters_diff(data):
    data = sorted([int(x) for x in data])

    diff_1 = 0
    diff_3 = 1

    curr_value = 0

    for value in data:
        diff_1 += 1 if value - curr_value == 1 else 0
        diff_3 += 1 if value - curr_value == 3 else 0

        curr_value = value

    return diff_1 * diff_3


class TestClass():

    def test_adapters_diff_1(self):
        data = [
            '16',
            '10',
            '15',
            '5',
            '1',
            '11',
            '7',
            '19',
            '6',
            '12',
            '4'
        ]

        assert adapters_diff(data) == 35

    def test_adapters_diff_2(self):
        data = [
            '28',
            '33',
            '18',
            '42',
            '31',
            '14',
            '46',
            '20',
            '48',
            '47',
            '24',
            '23',
            '49',
            '45',
            '19',
            '38',
            '39',
            '11',
            '1',
            '32',
            '25',
            '35',
            '8',
            '17',
            '7',
            '9',
            '4',
            '2',
            '34',
            '10',
            '3'
        ]

        assert adapters_diff(data) == 220


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = adapters_diff(data)
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys


def adapters_arrangements(data):
    data = [int(x) for x in data]

    data.append(0)
    data.append(max(data) + 3)

    data = sorted(data)

    arrangements = [1]

    for i in range(1, len(data)):
        value = data[i]
        ind = i - 1
        cnt = 0

        while ind >= 0 and value - data[ind] <= 3:
            cnt += arrangements[ind]
            ind -= 1

        arrangements.append(cnt)

    return arrangements[-1]


class TestClass():

    def test_adapters_arrangements_1(self):
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

        assert adapters_arrangements(data) == 8

    def test_adapters_arrangements_2(self):
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

        assert adapters_arrangements(data) == 19208


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = adapters_arrangements(data)
    print(result)


if __name__ == '__main__':
    main()

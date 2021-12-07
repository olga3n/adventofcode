#!/usr/bin/env python3

import sys


def optimal_move_fuel(data: str) -> int:

    values = list(map(int, data.split(',')))
    center = sorted(values)[len(values) // 2]

    return sum([abs(x - center) for x in values])


class TestClass():

    def test_1(self):
        data = '16,1,2,0,4,2,7,1,2,14'

        assert optimal_move_fuel(data) == 37


def main():
    data = next(sys.stdin).strip()
    result = optimal_move_fuel(data)
    print(result)


if __name__ == '__main__':
    main()

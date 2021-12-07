#!/usr/bin/env python3

import sys


def optimal_move_fuel(data: str) -> int:

    values = list(map(int, data.split(',')))
    min_score = 0

    for i in range(min(values), max(values) + 1):
        score = sum([abs(x - i) * (abs(x - i) + 1) // 2 for x in values])
        if i == 0 or min_score > score:
            min_score = score

    return min_score


class TestClass():

    def test_1(self):
        data = '16,1,2,0,4,2,7,1,2,14'

        assert optimal_move_fuel(data) == 168


def main():
    data = next(sys.stdin).strip()
    result = optimal_move_fuel(data)
    print(result)


if __name__ == '__main__':
    main()

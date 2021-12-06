#!/usr/bin/env python3

import sys


def fish_for_period(data: str, days: int = 256) -> int:

    fish_info = map(int, data.split(','))
    fish_freq = [0] * 9

    for fish in fish_info:
        fish_freq[fish] += 1

    for day in range(days):
        new_fish_freq = [0] * 9

        for fish_status in range(9):
            new_fish_freq[fish_status - 1] += fish_freq[fish_status]

            if fish_status == 0:
                new_fish_freq[6] += fish_freq[fish_status]

        fish_freq = new_fish_freq

    return sum(fish_freq)


class TestClass():

    def test_1(self):
        data = '3,4,3,1,2'

        assert fish_for_period(data) == 26984457539


def main():
    data = next(sys.stdin).strip()
    result = fish_for_period(data)
    print(result)


if __name__ == '__main__':
    main()

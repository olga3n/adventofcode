#!/usr/bin/env python3

import sys
from typing import Iterable


def line_score(line: str) -> int:
    symbols, values = line.split()
    values = list(map(int, values.split(',')))
    profile = [0] * (len(symbols) + 1)

    for i, char in enumerate(symbols):
        profile[i] = 1
        if char == '#':
            break

    for size_i, size in enumerate(values):
        new_profile = [0] * (len(symbols) + 1)

        for i in range(len(profile)):
            if profile[i] == 0 or profile[i] == '.':
                continue
            if i + size > len(symbols):
                continue
            if all(symbols[index] != '.' for index in range(i, i + size)):
                new_profile[i + size] += profile[i]

        profile = new_profile

        if size_i == len(values) - 1:
            break

        new_profile = [0] * (len(symbols) + 1)

        for i in range(len(symbols)):
            if profile[i] == 0 or symbols[i] == '#':
                continue

            for j in range(i + 1, len(symbols)):
                if symbols[j] == '?':
                    new_profile[j] += profile[i]
                if symbols[j] == '#':
                    new_profile[j] += profile[i]
                    break

        profile = new_profile

    result = 0

    for i in range(len(profile)):
        if profile[i] == 0:
            continue
        if i == len(profile) - 1:
            result += profile[i]
            continue
        if all(symbols[index] != '#' for index in range(i, len(symbols))):
            result += profile[i]

    return result


def total_score(data: Iterable[str]) -> int:
    return sum(line_score(line) for line in data)


def test_line_score():
    data = [
        '???.### 1,1,3',
        '.??..??...?##. 1,1,3',
        '?#?#?#?#?#?#?#? 1,3,1,6',
        '????.#...#... 4,1,1',
        '????.######..#####. 1,6,5',
        '?###???????? 3,2,1',
    ]
    assert line_score(data[0]) == 1
    assert line_score(data[1]) == 4
    assert line_score(data[2]) == 1
    assert line_score(data[3]) == 1
    assert line_score(data[4]) == 4
    assert line_score(data[5]) == 10


def test_total_score():
    data = [
        '???.### 1,1,3',
        '.??..??...?##. 1,1,3',
        '?#?#?#?#?#?#?#? 1,3,1,6',
        '????.#...#... 4,1,1',
        '????.######..#####. 1,6,5',
        '?###???????? 3,2,1',
    ]
    assert total_score(data) == 21


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = total_score(data)
    print(result)


if __name__ == '__main__':
    main()

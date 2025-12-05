#!/usr/bin/env python3

import sys
import bisect
from typing import Iterable, List, Tuple


def parse_lines(
    lines: Iterable[str],
) -> Tuple[List[Tuple[int, int]], List[int]]:

    values_flag = False
    ranges, values = [], []

    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            values_flag = True
            continue
        if values_flag:
            values.append(int(line))
        else:
            left, right = line.split('-')
            ranges.append((int(left), int(right)))

    return ranges, values


def minimized_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    new_ranges = []
    prev_range = None

    for next_range in ranges:
        if prev_range:
            if prev_range[0] <= next_range[0] <= prev_range[1]:
                prev_range = (
                    prev_range[0],
                    max(prev_range[1], next_range[1])
                )
            else:
                new_ranges.append(prev_range)
                prev_range = next_range
        else:
            prev_range = next_range

    if prev_range:
        new_ranges.append(prev_range)

    return new_ranges


def fresh_ingredients(ranges: List[Tuple[int, int]], values: List[int]) -> int:
    result = 0

    ranges.sort()
    ranges = minimized_ranges(ranges)

    for value in values:
        index = bisect.bisect_left(ranges, (value, 0))
        if index > 0:
            left, right = ranges[index - 1]
            if left <= value <= right:
                result += 1
                continue
        if index < len(ranges):
            left, right = ranges[index]
            if left <= value <= right:
                result += 1
                continue

    return result


def test_fresh_ingredients():
    lines = [
        '3-5',
        '10-14',
        '16-20',
        '12-18',
        '',
        '1',
        '5',
        '8',
        '11',
        '17',
        '32',
    ]
    assert 3 == fresh_ingredients(*parse_lines(lines))


def main():
    lines = sys.stdin
    result = fresh_ingredients(*parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()

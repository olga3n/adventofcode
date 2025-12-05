#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple


def parse_lines(lines: Iterable[str]) -> List[Tuple[int, int]]:
    ranges = []

    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            break
        left, right = line.split('-')
        ranges.append((int(left), int(right)))

    return ranges


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


def fresh_ingredients(ranges: List[Tuple[int, int]]) -> int:
    ranges.sort()
    ranges = minimized_ranges(ranges)
    return sum(right - left + 1 for left, right in ranges)


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
    assert 14 == fresh_ingredients(parse_lines(lines))


def main():
    lines = sys.stdin
    result = fresh_ingredients(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()

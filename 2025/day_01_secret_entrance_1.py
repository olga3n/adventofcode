#!/usr/bin/env python3

import sys
from typing import Iterable


def parse_lines(lines: Iterable[str]) -> Iterable[int]:
    for line in lines:
        value = int(line[1:])
        yield (-value if line.startswith('L') else value)


def turns(values: Iterable[int], start=50) -> Iterable[int]:
    current_angle = start
    for value in values:
        current_angle += value
        current_angle %= 100
        yield current_angle


def zero_turns(values: Iterable[int]) -> int:
    return sum(1 for x in turns(values) if x == 0)


def test_zero_turns():
    lines = [
        'L68',
        'L30',
        'R48',
        'L5',
        'R60',
        'L55',
        'L1',
        'L99',
        'R14',
        'L82',
    ]
    assert 3 == zero_turns(parse_lines(lines))


def main():
    lines = sys.stdin
    result = zero_turns(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()

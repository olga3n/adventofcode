#!/usr/bin/env python3

import sys
from typing import Iterable, Tuple


def parse_lines(lines: Iterable[str]) -> Iterable[int]:
    for line in lines:
        value = int(line[1:])
        yield (-value if line.startswith('L') else value)


def turns(values: Iterable[int], start=50) -> Iterable[Tuple[int, int]]:
    current_angle = start

    for value in values:
        zero_turns = abs(current_angle + value) // 100
        if value < 0 and current_angle > 0 and abs(value) >= current_angle:
            zero_turns += 1

        current_angle += value
        current_angle %= 100

        yield current_angle, zero_turns


def zero_turns(values: Iterable[int]) -> int:
    return sum(zero_turns for _, zero_turns in turns(values))


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
    assert 6 == zero_turns(parse_lines(lines))


def main():
    lines = sys.stdin
    result = zero_turns(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()

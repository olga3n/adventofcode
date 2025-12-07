#!/usr/bin/env python3

import sys
from typing import List, Tuple


def find_symbol(lines: List[str], symbol: str) -> Tuple[int, int]:
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == symbol:
                return (row, col)

    return (-1, -1)


def split_cnt(lines: List[str]) -> int:
    result = 0

    s_pos = find_symbol(lines, 'S')
    signals = {s_pos[1]}

    for row in range(s_pos[0] + 1, len(lines)):
        new_signals = set()

        for col in signals:
            if lines[row][col] == '.':
                new_signals.add(col)
            elif lines[row][col] == '^':
                result += 1
                new_signals.add(col - 1)
                new_signals.add(col + 1)

        signals = new_signals

    return result


def test_split_cnt():
    lines = [
        '.......S.......',
        '...............',
        '.......^.......',
        '...............',
        '......^.^......',
        '...............',
        '.....^.^.^.....',
        '...............',
        '....^.^...^....',
        '...............',
        '...^.^...^.^...',
        '...............',
        '..^...^.....^..',
        '...............',
        '.^.^.^.^.^...^.',
        '...............',
    ]
    assert 21 == split_cnt(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = split_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()

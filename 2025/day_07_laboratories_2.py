#!/usr/bin/env python3

import sys
from typing import Dict, List, Tuple


def find_symbol(lines: List[str], symbol: str) -> Tuple[int, int]:
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == symbol:
                return (row, col)

    return (-1, -1)


def timeline_cnt(lines: List[str]) -> int:
    s_pos = find_symbol(lines, 'S')
    signals = {s_pos[1]: 1}

    for row in range(s_pos[0] + 1, len(lines)):
        new_signals: Dict[int, int] = {}

        for col, cnt in signals.items():
            if lines[row][col] == '.':
                new_signals[col] = new_signals.get(col, 0) + cnt
            elif lines[row][col] == '^':
                new_signals[col - 1] = new_signals.get(col - 1, 0) + cnt
                new_signals[col + 1] = new_signals.get(col + 1, 0) + cnt

        signals = new_signals

    return sum(signals.values())


def test_timeline_cnt():
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
    assert 40 == timeline_cnt(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = timeline_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()

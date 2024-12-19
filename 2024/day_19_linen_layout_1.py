#!/usr/bin/env python3

import sys
from typing import Iterable


def parse_data(lines: Iterable[str]) -> tuple[set[str], list[str]]:
    patterns = []
    designs = []

    flag = False

    for line in lines:
        if len(line) == 0:
            flag = True
        elif not flag:
            patterns.extend(line.split(', '))
        else:
            designs.append(line)

    return set(patterns), designs


def is_possible(patterns: set[str], design: str) -> bool:
    stack = [0]
    visited = set()
    max_pattern_len = max(len(pattern) for pattern in patterns)

    while len(stack):
        start = stack.pop()

        if start in visited:
            continue

        visited.add(start)

        for end in range(start + 1, start + max_pattern_len + 1):
            if design[start: end] in patterns:
                if end > len(design):
                    break
                if end == len(design):
                    return True
                stack.append(end)

    return False


def possible_designs(patterns: set[str], designs: list[str]) -> int:
    return sum(1 for design in designs if is_possible(patterns, design))


def test_possible_seq_cnt():
    lines = [
        'r, wr, b, g, bwu, rb, gb, br',
        '',
        'brwrr',
        'bggr',
        'gbbr',
        'rrbgbr',
        'ubwu',
        'bwurrg',
        'brgr',
        'bbrgwb',
    ]
    assert 6 == possible_designs(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = possible_designs(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()

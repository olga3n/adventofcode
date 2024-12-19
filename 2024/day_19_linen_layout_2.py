#!/usr/bin/env python3

import sys
import heapq
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


def possible_combinations(patterns: set[str], design: str) -> int:
    h = [0]
    dp = [0] * len(design)
    dp[0] = 1

    visited = [False] * len(design)
    max_pattern_len = max(len(pattern) for pattern in patterns)
    result = 0

    while len(h):
        start = heapq.heappop(h)

        if visited[start]:
            continue

        visited[start] = True

        for end in range(start + 1, start + max_pattern_len + 1):
            if design[start: end] in patterns:
                if end > len(design):
                    break
                if end == len(design):
                    result += dp[start]
                    break
                dp[end] += dp[start]
                heapq.heappush(h, end)

    return result


def possible_designs(patterns: set[str], designs: list[str]) -> int:
    return sum(possible_combinations(patterns, design) for design in designs)


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
    assert 16 == possible_designs(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = possible_designs(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()

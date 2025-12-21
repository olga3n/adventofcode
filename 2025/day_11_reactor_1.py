#!/usr/bin/env python3

import sys
from typing import Dict, Iterable, Set


def parse_lines(lines: Iterable[str]) -> Dict[str, Set[str]]:
    graph = {}

    for line in lines:
        line = line.rstrip()
        part_1, part_2 = line.split(': ')
        graph[part_1] = set(part_2.split())

    return graph


def all_paths(
    graph: Dict[str, Set[str]], start='you', end='out',
) -> int:

    dp = {}
    dp[start] = 1

    result = 0

    while len(dp):
        dp_new = {}

        for v_in in dp:
            if v_in not in graph:
                continue
            for v_out in graph[v_in]:
                dp_new[v_out] = dp_new.get(v_out, 0) + dp[v_in]

        dp = dp_new
        result += dp.get(end, 0)

    return result


def test_all_paths():
    lines = [
        'aaa: you hhh',
        'you: bbb ccc',
        'bbb: ddd eee',
        'ccc: ddd eee fff',
        'ddd: ggg',
        'eee: out',
        'fff: out',
        'ggg: out',
        'hhh: ccc fff iii',
        'iii: out',
    ]
    assert 5 == all_paths(parse_lines(lines))


def main():
    lines = sys.stdin
    result = all_paths(parse_lines(lines))
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
from typing import Dict, Iterable
from dataclasses import dataclass


@dataclass
class Node:
    left: str
    right: str


def parse_graph(data: Iterable[str]) -> Dict[str, Node]:
    graph = {}

    for line in data:
        if not len(line):
            continue
        label, rest = line.split(' = ')
        left, right = rest.split(', ')
        graph[label] = Node(left[1:], right[:-1])

    return graph


def steps(data: Iterable[str], start='AAA', end='ZZZ') -> int:
    directions = next(data)
    graph = parse_graph(data)

    index, cnt, node = 0, 0, start

    while node != end:
        node = (
            graph[node].left if directions[index] == 'L'
            else graph[node].right
        )
        cnt += 1
        index += 1
        index %= len(directions)

    return cnt


def test_steps():
    data = [
        'RL',
        '',
        'AAA = (BBB, CCC)',
        'BBB = (DDD, EEE)',
        'CCC = (ZZZ, GGG)',
        'DDD = (DDD, DDD)',
        'EEE = (EEE, EEE)',
        'GGG = (GGG, GGG)',
        'ZZZ = (ZZZ, ZZZ)',
    ]
    assert steps(iter(data)) == 2

    data = [
        'LLR',
        '',
        'AAA = (BBB, BBB)',
        'BBB = (AAA, ZZZ)',
        'ZZZ = (ZZZ, ZZZ)',
    ]
    assert steps(iter(data)) == 6


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = steps(data)
    print(result)


if __name__ == '__main__':
    main()

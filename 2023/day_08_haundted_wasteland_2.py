#!/usr/bin/env python3

import sys
import math
from typing import Dict, Iterable, Optional
from dataclasses import dataclass


@dataclass
class Node:
    left: str
    right: str


@dataclass
class HistoryItem:
    first: Optional[int] = None
    second: Optional[int] = None

    def is_ready(self) -> bool:
        return (
            self.first is not None and
            self.second is not None
        )


def parse_graph(data: Iterable[str]) -> Dict[str, Node]:
    graph = {}

    for line in data:
        if not len(line):
            continue
        label, rest = line.split(' = ')
        left, right = rest.split(', ')
        graph[label] = Node(left[1:], right[:-1])

    return graph


def steps(data: Iterable[str], start_suffix='A', end_suffix='Z') -> int:
    directions = next(data)
    graph = parse_graph(data)

    index, cnt = 0, 0
    nodes = [label for label in graph if label[-1] == start_suffix]

    history = {}

    while True:
        for i in range(len(nodes)):
            nodes[i] = (
                graph[nodes[i]].left if directions[index] == 'L'
                else graph[nodes[i]].right
            )

        cnt += 1
        index += 1
        index %= len(directions)

        if all(label[-1] == end_suffix for label in nodes):
            break

        for i, label in enumerate(nodes):
            if label[-1] == end_suffix:
                if index not in history:
                    history[index] = [
                        HistoryItem() for j in range(len(nodes))
                    ]
                if not history[index][i].first:
                    history[index][i].first = cnt
                elif not history[index][i].second:
                    history[index][i].second = cnt

        for i in history:
            if all(item.is_ready() for item in history[i]):
                values = [item.second - item.first for item in history[i]]
                return i + math.lcm(*values)

    return cnt


def test_steps():
    data = [
        'LR',
        '',
        '11A = (11B, XXX)',
        '11B = (XXX, 11Z)',
        '11Z = (11B, XXX)',
        '22A = (22B, XXX)',
        '22B = (22C, 22C)',
        '22C = (22Z, 22Z)',
        '22Z = (22B, 22B)',
        'XXX = (XXX, XXX)',
    ]
    assert steps(iter(data)) == 6


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = steps(data)
    print(result)


if __name__ == '__main__':
    main()

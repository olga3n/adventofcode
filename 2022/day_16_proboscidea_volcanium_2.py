#!/usr/bin/env python3

import sys
import re
from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Set


@dataclass
class GraphNode:
    rate: int
    tunnels: List[str]


@dataclass
class Step:
    score: int
    name_1: str
    name_2: str
    opened: Set[str]
    minutes: int


def max_pressure(
    data: Iterable[str], minutes: int = 26, start: str = 'AA'
) -> int:
    parse_re = (
        r'Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.*)'
    )

    nodes = {}
    nodes_to_open = set()

    for line in data:
        matched = re.match(parse_re, line.strip())
        if matched:
            valve, rate, tunnels = matched.groups()
            rate = int(rate)
            tunnels = tunnels.split(', ')
            nodes[valve] = GraphNode(rate, tunnels)
            if rate > 0:
                nodes_to_open.add(valve)

    steps = deque([Step(0, start, start, set(), minutes)])

    visited = set()
    result = 0

    while steps:
        step = steps.popleft()

        if (step.name_1, step.name_2, step.score) in visited:
            continue

        visited.add((step.name_1, step.name_2, step.score))

        if step.minutes == 0 or len(step.opened) == len(nodes_to_open):
            result = max(result, step.score)
            continue

        variants_1 = []
        variants_2 = []

        if step.name_1 not in step.opened and step.name_1 in nodes_to_open:
            score = nodes[step.name_1].rate * (step.minutes - 1)
            variants_1.append((score, step.name_1, step.name_1))

        if step.name_2 not in step.opened and step.name_2 in nodes_to_open:
            score = nodes[step.name_2].rate * (step.minutes - 1)
            variants_2.append((score, step.name_2, step.name_2))

        for tunnel in nodes[step.name_1].tunnels:
            variants_1.append((0, tunnel, ''))

        for tunnel in nodes[step.name_2].tunnels:
            variants_2.append((0, tunnel, ''))

        for score_1, name_1, open_1 in variants_1:
            for score_2, name_2, open_2 in variants_2:

                opened = set(step.opened)

                if open_1:
                    opened.add(open_1)

                if open_2:
                    opened.add(open_2)

                if open_1 == open_2 and open_1 != '':
                    continue

                next_step = Step(
                    step.score + score_1 + score_2,
                    name_1,
                    name_2,
                    opened,
                    step.minutes - 1
                )

                next_tuple = (
                    next_step.name_1, next_step.name_2, next_step.score
                )

                if next_tuple not in visited:
                    steps.append(next_step)

    return result


def test_max_pressure():
    data = [
        'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB',
        'Valve BB has flow rate=13; tunnels lead to valves CC, AA',
        'Valve CC has flow rate=2; tunnels lead to valves DD, BB',
        'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE',
        'Valve EE has flow rate=3; tunnels lead to valves FF, DD',
        'Valve FF has flow rate=0; tunnels lead to valves EE, GG',
        'Valve GG has flow rate=0; tunnels lead to valves FF, HH',
        'Valve HH has flow rate=22; tunnel leads to valve GG',
        'Valve II has flow rate=0; tunnels lead to valves AA, JJ',
        'Valve JJ has flow rate=21; tunnel leads to valve II'
    ]

    assert max_pressure(data) == 1707


def main():
    data = sys.stdin
    result = max_pressure(data)
    print(result)


if __name__ == '__main__':
    main()

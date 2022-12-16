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
    name: str
    opened: Set[str]
    minutes: int


def max_pressure(
    data: Iterable[str], minutes: int = 30, start: str = 'AA'
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

    steps = deque([Step(0, start, set(), minutes)])

    visited = set()
    result = 0

    while steps:
        step = steps.popleft()

        if (step.name, step.score) in visited:
            continue

        visited.add((step.name, step.score))

        if step.minutes == 0 or len(step.opened) == len(nodes_to_open):
            result = max(result, step.score)
            continue

        if step.name not in step.opened and step.name in nodes_to_open:
            score = step.score + nodes[step.name].rate * (step.minutes - 1)
            opened = set(step.opened)
            opened.add(step.name)
            next_step = Step(
                score, step.name, opened, step.minutes - 1
            )
            if (next_step.name, next_step.score) not in visited:
                steps.append(next_step)

        for tunnel in nodes[step.name].tunnels:
            next_step = Step(
                step.score, tunnel, step.opened, step.minutes - 1
            )
            if (next_step.name, next_step.score) not in visited:
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

    assert max_pressure(data) == 1651


def main():
    data = sys.stdin
    result = max_pressure(data)
    print(result)


if __name__ == '__main__':
    main()

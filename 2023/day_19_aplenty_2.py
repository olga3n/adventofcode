#!/usr/bin/env python3

import sys
from typing import Iterable, Callable, Tuple, Dict, List


def parse_data(data: Iterable[str]) -> Dict[str, List[Callable]]:
    graph = {}

    for line in data:
        if not len(line) or line.startswith('{'):
            continue

        label, tail = line[:-1].split('{')
        graph[label] = []

        for condition in tail.split(','):
            if ':' in condition:
                head, out = condition.split(':')
                test, cmp, value = head[0], head[1], int(head[2:])
                graph[label].append(
                    lambda intervals, test=test, cmp=cmp, value=value, out=out:
                        (*upd_intervals(intervals, test, cmp, value), out)
                )
            else:
                out = condition
                graph[label].append(
                    lambda intervals, out=out: (intervals, None, out)
                )

    return graph


def upd_intervals(
    intervals: Dict[str, Tuple[int, int]], label: str, cmp: str, value: str
) -> Tuple[Dict[str, Tuple[int, int]], Dict[str, Tuple[int, int]]]:
    a_intervals = {}
    r_intervals = {}

    for symbol, (left, right) in intervals.items():
        if symbol != label or (left, right) == (-1, -1):
            a_intervals[symbol] = intervals[symbol]
            r_intervals[symbol] = intervals[symbol]
            continue

        accepted = (-1, -1)
        rejected = (-1, -1)

        if cmp == '<' and left < value <= right:
            accepted = left, value - 1
            rejected = value, right
        elif cmp == '<' and value <= left:
            rejected = left, right
        elif cmp == '>' and left <= value < right:
            accepted = value + 1, right
            rejected = left, value
        elif cmp == '>' and value >= right:
            rejected = left, right
        else:
            accepted = left, right

        a_intervals[symbol] = accepted
        r_intervals[symbol] = rejected

    return a_intervals, r_intervals


def total_combinations(data: Iterable[str]) -> int:
    graph = parse_data(data)

    label = 'in'
    intervals = {char: (1, 4000) for char in 'xmas'}

    states = [(label, intervals)]
    results = []

    while len(states):
        label, intervals = states.pop()
        if label == 'A':
            results.append(intervals)
            continue
        if label == 'R':
            continue

        r_intervals = intervals

        for call in graph[label]:
            if r_intervals:
                a_intervals, r_intervals, out = call(r_intervals)
                states.append((out, a_intervals))

    result = 0

    for item in results:
        value = 1
        for char in 'xmas':
            if item[char] != (-1,  -1):
                value *= item[char][1] - item[char][0] + 1
            else:
                value = 0
        result += value

    return result


def test_total_combinations():
    data = [
        'px{a<2006:qkq,m>2090:A,rfg}',
        'pv{a>1716:R,A}',
        'lnx{m>1548:A,A}',
        'rfg{s<537:gd,x>2440:R,A}',
        'qs{s>3448:A,lnx}',
        'qkq{x<1416:A,crn}',
        'crn{x>2662:A,R}',
        'in{s<1351:px,qqz}',
        'qqz{s>2770:qs,m<1801:hdj,R}',
        'gd{a>3333:R,R}',
        'hdj{m>838:A,pv}',
    ]
    assert total_combinations(data) == 167409079868000


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = total_combinations(data)
    print(result)


if __name__ == '__main__':
    main()

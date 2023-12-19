#!/usr/bin/env python3

import sys
from typing import Iterable, Callable, Tuple, Dict, List


def parse_data(
    data: Iterable[str]
) -> Tuple[Dict[str, List[Callable]], List[Dict[str, int]]]:
    graph, parts = {}, []

    for line in data:
        if not len(line):
            continue

        if line.startswith('{'):
            part = {}

            for pair in line[1:-1].split(','):
                key, value = pair.split('=')
                part[key] = int(value)

            parts.append(part)
        else:
            label, tail = line[:-1].split('{')
            graph[label] = []

            for condition in tail.split(','):
                if ':' in condition:
                    head, out = condition.split(':')
                    test, cmp, value = head[0], head[1], int(head[2:])
                    graph[label].append(
                        lambda part, test=test, cmp=cmp, value=value, out=out:
                            out if (cmp == '<' and part[test] < value) or
                            (cmp == '>' and part[test] > value) else None
                    )
                else:
                    out = condition
                    graph[label].append(
                        lambda part, out=out: out
                    )

    return graph, parts


def part_rating(graph: Dict[str, List[Callable]], part: Dict[str, int]) -> int:
    label = 'in'

    while label != 'A' and label != 'R':
        for condition in graph[label]:
            out = condition(part)
            if out is not None:
                label = out
                break

    return sum(part.values()) if label == 'A' else 0


def total_rating(data: Iterable[str]) -> int:
    graph, parts = parse_data(data)
    return sum(part_rating(graph, part) for part in parts)


def test_total_rating():
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
        '',
        '{x=787,m=2655,a=1222,s=2876}',
        '{x=1679,m=44,a=2067,s=496}',
        '{x=2036,m=264,a=79,s=2244}',
        '{x=2461,m=1339,a=466,s=291}',
        '{x=2127,m=1623,a=2188,s=1013}',
    ]
    assert total_rating(data[:12] + [data[12]]) == 7540
    assert total_rating(data[:12] + [data[14]]) == 4623
    assert total_rating(data[:12] + [data[16]]) == 6951
    assert total_rating(data) == 19114


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = total_rating(data)
    print(result)


if __name__ == '__main__':
    main()

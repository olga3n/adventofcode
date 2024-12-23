#!/usr/bin/env python3

import sys
from typing import Iterable


def parse_connections(lines: Iterable[str]) -> dict[str, set[str]]:
    connections: dict[str, set[str]] = {}

    for line in lines:
        one, two = line.split('-')
        if one not in connections:
            connections[one] = {two}
        else:
            connections[one].add(two)

        if two not in connections:
            connections[two] = {one}
        else:
            connections[two].add(one)

    return connections


def interconnections(connections: dict[str, set[str]]) -> str:
    candidates = set()

    for k1, conn_lst in connections.items():
        for k2 in conn_lst:
            for k3 in connections[k2]:
                if k1 in connections[k3]:
                    candidates.add(tuple(sorted((k1, k2, k3))))

    while True:
        new_candidates = set()

        for tpl in candidates:
            k1 = tpl[0]
            s = set(tpl)
            for v in connections[k1]:
                if v in s:
                    continue
                if s.issubset(set(connections[v]).intersection(s)):
                    new_candidate = s.copy()
                    new_candidate.add(v)
                    new_candidates.add(tuple(sorted(new_candidate)))

        if len(new_candidates) == 0:
            break

        candidates = new_candidates

    click = next(iter(candidates))

    return ",".join(click)


def test_interconnections():
    lines = [
        'kh-tc',
        'qp-kh',
        'de-cg',
        'ka-co',
        'yn-aq',
        'qp-ub',
        'cg-tb',
        'vc-aq',
        'tb-ka',
        'wh-tc',
        'yn-cg',
        'kh-ub',
        'ta-co',
        'de-co',
        'tc-td',
        'tb-wq',
        'wh-td',
        'ta-ka',
        'td-qp',
        'aq-cg',
        'wq-ub',
        'ub-vc',
        'de-ta',
        'wq-aq',
        'wq-vc',
        'wh-yn',
        'ka-de',
        'kh-ta',
        'co-tc',
        'wh-qp',
        'tb-vc',
        'td-yn',
    ]
    assert "co,de,ka,ta" == interconnections(parse_connections(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = interconnections(parse_connections(lines))
    print(result)


if __name__ == '__main__':
    main()

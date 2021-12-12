#!/usr/bin/env python3

import sys
from typing import List, Dict


def paths_count(data: List[str]) -> int:

    result = 0
    edges: Dict[str, List[str]] = {}

    for line in data:
        v1, v2 = line.split('-')
        edges[v1] = edges.get(v1, []) + [v2]
        edges[v2] = edges.get(v2, []) + [v1]

    stack = [({'start'}, None, 'start')]

    while len(stack):
        used, special, v = stack.pop()

        for vi in edges.get(v, []):
            if vi == 'end':
                result += 1
            elif vi.islower() and vi not in used:
                stack.append((used.union({vi}), special, vi))
            elif vi.islower() and not special and vi not in {'start', 'end'}:
                stack.append((used, vi, vi))
            elif vi.isupper():
                stack.append((used, special, vi))

    return result


class TestClass():

    def test_1(self):
        data = [
            'start-A',
            'start-b',
            'A-c',
            'A-b',
            'b-d',
            'A-end',
            'b-end',
        ]

        assert paths_count(data) == 36

    def test_2(self):
        data = [
            'dc-end',
            'HN-start',
            'start-kj',
            'dc-start',
            'dc-HN',
            'LN-dc',
            'HN-end',
            'kj-sa',
            'kj-HN',
            'kj-dc',
        ]

        assert paths_count(data) == 103

    def test_3(self):
        data = [
            'fs-end',
            'he-DX',
            'fs-he',
            'start-DX',
            'pj-DX',
            'end-zg',
            'zg-sl',
            'zg-pj',
            'pj-he',
            'RW-he',
            'fs-DX',
            'pj-RW',
            'zg-RW',
            'start-pj',
            'he-WI',
            'zg-he',
            'pj-fs',
            'start-RW',
        ]

        assert paths_count(data) == 3509


def main():
    data = [x.strip() for x in sys.stdin]
    result = paths_count(data)
    print(result)


if __name__ == '__main__':
    main()

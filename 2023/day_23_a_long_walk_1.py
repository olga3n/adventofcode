#!/usr/bin/env python3

import sys

from typing import List

SLOPES = {
    '^': (-1, 0),
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1),
}


def max_path(data: List[str]) -> int:
    start = (0, data[0].find('.'))
    end = (len(data) - 1, data[-1].find('.'))

    stack = [(start, 0, 0)]
    visited = set()

    result = 0

    while stack:
        pos, path, state = stack.pop()

        if state == 1:
            visited.remove(pos)
            continue

        if pos == end:
            result = max(result, path)
            continue

        visited.add(pos)
        stack.append((pos, path, 1))

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            x = pos[0] + dx
            y = pos[1] + dy
            if not 0 <= x < len(data):
                continue
            if not 0 <= y < len(data[0]):
                continue
            if data[x][y] == '#':
                continue
            new_path = path + 1
            if data[x][y] in SLOPES:
                dx, dy = SLOPES[data[x][y]]
                x += dx
                y += dy
                new_path += 1
            if (x, y) in visited:
                continue
            stack.append(((x, y), new_path, 0))

    return result


def test_max_path():
    data = [
        '#.#####################',
        '#.......#########...###',
        '#######.#########.#.###',
        '###.....#.>.>.###.#.###',
        '###v#####.#v#.###.#.###',
        '###.>...#.#.#.....#...#',
        '###v###.#.#.#########.#',
        '###...#.#.#.......#...#',
        '#####.#.#.#######.#.###',
        '#.....#.#.#.......#...#',
        '#.#####.#.#.#########v#',
        '#.#...#...#...###...>.#',
        '#.#.#v#######v###.###v#',
        '#...#.>.#...>.>.#.###.#',
        '#####v#.#.###v#.#.###.#',
        '#.....#...#...#.#.#...#',
        '#.#########.###.#.#.###',
        '#...###...#...#...#.###',
        '###.###.#.###v#####v###',
        '#...#...#.#.>.>.#.>.###',
        '#.###.###.#.###.#.#v###',
        '#.....###...###...#...#',
        '#####################.#',
    ]
    assert max_path(data) == 94


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = max_path(data)
    print(result)


if __name__ == '__main__':
    main()

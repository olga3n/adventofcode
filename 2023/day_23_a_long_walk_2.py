#!/usr/bin/env python3

import sys

from typing import List, Tuple, Set


def find_paths(
    data: List[str], start: Tuple[int, int], end_set: Set[Tuple[int, int]]
):
    stack = [(start, 0, 0)]
    visited = set()

    while stack:
        pos, path, state = stack.pop()

        if state == 1:
            visited.remove(pos)
            continue

        if pos in end_set and pos != start:
            yield (pos, path, set(visited))
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
            if (x, y) in visited:
                continue
            stack.append(((x, y), path + 1, 0))


def max_path(data: List[str]) -> int:
    start = (0, data[0].find('.'))
    end = (len(data) - 1, data[-1].find('.'))

    forks = []

    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == '#':
                continue

            adj = []

            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                xx = x + dx
                yy = y + dy
                if not 0 <= xx < len(data):
                    continue
                if not 0 <= yy < len(data[0]):
                    continue
                if data[xx][yy] == '#':
                    continue
                adj.append((xx, yy))

            if len(adj) != 2:
                forks.append((x, y))

    graph = {}

    for start_pos in forks:
        graph[start_pos] = []
        for end_pos, path, visited in find_paths(data, start_pos, forks):
            graph[start_pos].append((end_pos, path, visited))

    stack = [(start, 0, 0)]
    visited = set()

    result = 0

    while stack:
        pos, path, state = stack.pop()

        if state == 1:
            visited.remove(pos)
            continue

        if pos == end:
            if path > result:
                print("found path", path, file=sys.stderr)
            result = max(result, path)
            continue

        visited.add(pos)
        stack.append((pos, path, 1))

        for end_pos, new_path, _ in graph[pos]:
            if end_pos not in visited:
                stack.append((end_pos, path + new_path, 0))

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
    assert max_path(data) == 154


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = max_path(data)
    print(result)


if __name__ == '__main__':
    main()

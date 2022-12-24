#!/usr/bin/env python3

import sys
from collections import deque
from typing import List, Dict, Set, Tuple


def shortest_path(data: List[str]) -> int:
    data = [line.rstrip() for line in data]
    blizzards: Dict[str, List[Tuple[int, int]]] = {
        '>': [], '<': [], '^': [], 'v': []
    }

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != '.' and data[i][j] != '#':
                blizzards[data[i][j]].append((i, j))

    blizzads_pos_1 = []
    current_blizzards_up = blizzards['^']
    current_blizzards_down = blizzards['v']
    size = len(data) - 2

    for _ in range(size):
        positions = (
            set(current_blizzards_up).union(set(current_blizzards_down))
        )
        blizzads_pos_1.append(positions)
        current_blizzards_up = [
            (1 + ((x - 2) % size), y) for x, y in current_blizzards_up
        ]
        current_blizzards_down = [
            (1 + (x % size), y) for x, y in current_blizzards_down
        ]

    blizzads_pos_2 = []
    current_blizzards_right = blizzards['>']
    current_blizzards_left = blizzards['<']
    size = len(data[0]) - 2

    for _ in range(len(data[0]) - 2):
        positions = (
            set(current_blizzards_right).union(set(current_blizzards_left))
        )
        blizzads_pos_2.append(positions)
        current_blizzards_right = [
            (x, 1 + (y % size)) for x, y in current_blizzards_right
        ]
        current_blizzards_left = [
            (x, 1 + ((y - 2) % size)) for x, y in current_blizzards_left
        ]

    state = (0, 1, 0, 0, 0)
    visited: Set[Tuple[int, int, int, int]] = set()
    queue = deque([state])
    part = 0

    while queue:
        x, y, tick_1, tick_2, steps = queue.popleft()

        if part == 0 and (x, y) == (len(data) - 1, len(data[0]) - 2):
            part = 1
            queue = deque([(x, y, tick_1, tick_2, steps)])
            visited = set()
            continue

        if part == 1 and (x, y) == (0, 1):
            part = 2
            queue = deque([(x, y, tick_1, tick_2, steps)])
            visited = set()
            continue

        if part == 2 and (x, y) == (len(data) - 1, len(data[0]) - 2):
            return steps

        if (x, y, tick_1, tick_2) in visited:
            continue

        visited.add((x, y, tick_1, tick_2))

        tick_1 = (tick_1 + 1) % (len(data) - 2)
        tick_2 = (tick_2 + 1) % (len(data[0]) - 2)

        for diff_x, diff_y in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)):
            xx = x + diff_x
            yy = y + diff_y
            if not 0 <= xx < len(data):
                continue
            if not 0 <= yy < len(data[0]):
                continue
            if data[xx][yy] == '#':
                continue
            if ((xx, yy) not in blizzads_pos_1[tick_1] and
                    (xx, yy) not in blizzads_pos_2[tick_2]):
                queue.append((xx, yy, tick_1, tick_2, steps + 1))

    return 0


def test_shortest_path():
    data = [
        '#.######',
        '#>>.<^<#',
        '#.<..<<#',
        '#>v.><>#',
        '#<^v^^>#',
        '######.#'
    ]

    assert shortest_path(data) == 54


def main():
    data = sys.stdin.readlines()
    result = shortest_path(data)
    print(result)


if __name__ == '__main__':
    main()

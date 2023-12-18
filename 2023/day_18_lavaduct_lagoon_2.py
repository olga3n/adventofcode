#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple, Set

DIFF = {
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0),
    'U': (-1, 0),
}


def parse_data(data: Iterable[str]) -> Tuple[str, int]:
    directions = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U'
    }
    for line in data:
        _, _, color = line.split()
        color = color[2:-1]
        direction = directions[color[-1]]
        yield direction, int(color[:-1], 16)


def check_area(
    field: List[List[str]], pos: Tuple[int, int]
) -> Set[Tuple[int, int]]:
    visited, is_internal = set(), True
    stack = [pos]
    while stack:
        pos = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            xx = pos[0] + dx
            yy = pos[1] + dy
            if not 0 <= xx < len(field):
                is_internal = False
                continue
            if not 0 <= yy < len(field[0]):
                is_internal = False
                continue
            if field[xx][yy] != '.':
                continue
            if (xx, yy) in visited:
                continue
            stack.append((xx, yy))
    return visited, is_internal


def total_lava(data: Iterable[str]) -> int:
    pos = (0, 0)
    set_x, set_y = {0}, {0}
    steps = list(parse_data(data))

    for direction, size in steps:
        dx, dy = DIFF[direction]
        pos = (
            pos[0] + dx * size,
            pos[1] + dy * size
        )
        set_x.add(pos[0])
        set_y.add(pos[1])
        set_x.add(pos[0] + 1)
        set_y.add(pos[1] + 1)

    min_x, min_y = min(set_x), min(set_y)

    rows = [item - min_x for item in sorted(set_x)]
    cols = [item - min_y for item in sorted(set_y)]

    field = []

    for i in range(len(rows)):
        field.append(['.'] * len(cols))

    start = (-min_x, -min_y)

    for direction, size in steps:
        dx, dy = DIFF[direction]
        end = (
            start[0] + dx * size,
            start[1] + dy * size
        )
        if dy == 0:
            i_col = cols.index(start[1])
            left, right = min(start[0], end[0]), max(start[0], end[0])
            for i_row, row in enumerate(rows):
                if left <= row <= right:
                    field[i_row][i_col] = '#'
        elif dx == 0:
            i_row = rows.index(start[0])
            left, right = min(start[1], end[1]), max(start[1], end[1])
            for i_col, col in enumerate(cols):
                if left <= col <= right:
                    field[i_row][i_col] = '#'
        start = end

    visited = set()

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == '.' and (i, j) not in visited:
                new_visited, is_internal = check_area(field, (i, j))
                if is_internal:
                    for xx, yy in new_visited:
                        field[xx][yy] = '#'
                visited.update(new_visited)

    result = 0

    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == '#':
                value = (rows[i + 1] - rows[i]) * (cols[j + 1] - cols[j])
                result += value

    return result


def test_total_lava():
    data = [
        'R 6 (#70c710)',
        'D 5 (#0dc571)',
        'L 2 (#5713f0)',
        'D 2 (#d2c081)',
        'R 2 (#59c680)',
        'D 2 (#411b91)',
        'L 5 (#8ceee2)',
        'U 2 (#caa173)',
        'L 1 (#1b58a2)',
        'U 2 (#caa171)',
        'R 2 (#7807d2)',
        'U 3 (#a77fa3)',
        'L 2 (#015232)',
        'U 2 (#7a21e3)',
    ]
    assert total_lava(data) == 952408144115


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = total_lava(data)
    print(result)


if __name__ == '__main__':
    main()

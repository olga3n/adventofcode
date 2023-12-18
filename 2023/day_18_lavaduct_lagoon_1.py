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
    for line in data:
        direction, size, _ = line.split()
        yield direction, int(size)


def next_step(
    field: List[List[str]], pos: Tuple[int, int], direction: str, size: int
) -> Tuple[List[List[str]], Tuple[int, int]]:
    dx, dy = DIFF[direction]

    new_field = []
    new_pos = pos

    if dx < 0 and size > new_pos[0]:
        extra_lines = size - new_pos[0]
        new_pos = (new_pos[0] + extra_lines, new_pos[1])
        for i in range(extra_lines):
            new_field.append(['.'] * len(field[0]))

    for line in field:
        new_field.append(line)

    if dx > 0 and size > len(field) - 1 - new_pos[0]:
        extra_lines = size - (len(field) - 1 - new_pos[0])
        for i in range(extra_lines):
            new_field.append(['.'] * len(field[0]))

    if dy < 0 and size > new_pos[1]:
        extra_cols = size - new_pos[1]
        new_pos = (new_pos[0], new_pos[1] + extra_cols)
        for i in range(len(new_field)):
            new_field[i] = ['.'] * extra_cols + new_field[i]

    if dy > 0 and size > len(field[0]) - 1 - new_pos[1]:
        extra_cols = size - (len(field[0]) - 1 - new_pos[1])
        for i in range(len(new_field)):
            new_field[i] = new_field[i] + ['.'] * extra_cols

    for i in range(size):
        new_pos = (
            new_pos[0] + dx,
            new_pos[1] + dy
        )
        new_field[new_pos[0]][new_pos[1]] = '#'

    return new_field, new_pos


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
    field, pos = [['#']], (0, 0)
    for direction, size in parse_data(data):
        field, pos = next_step(field, pos, direction, size)

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

    for line in field:
        result += sum(1 for char in line if char == '#')

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
    assert total_lava(data) == 62


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = total_lava(data)
    print(result)


if __name__ == '__main__':
    main()

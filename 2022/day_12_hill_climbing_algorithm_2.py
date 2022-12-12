#!/usr/bin/env python3

import sys
from collections import deque
from typing import List, Tuple


def find_pos(data: List[str], element) -> Tuple[int, int]:
    for row_index, line in enumerate(data):
        col_index = line.find(element)
        if col_index >= 0:
            return (row_index, col_index)
    return (-1, -1)


def find_all_pos(data: List[str], element) -> List[Tuple[int, int]]:
    result = []

    for row_index, line in enumerate(data):
        col_index = line.find(element)
        if col_index >= 0:
            result.append((row_index, col_index))

    return result


def find_neighbours(
    data: List[str], pos: Tuple[int, int]
) -> List[Tuple[int, int]]:

    result = []
    rows, cols = len(data), len(data[0])

    for diff_x, diff_y in {(-1, 0), (1, 0), (0, -1), (0, 1)}:
        new_pos = (
            pos[0] + diff_x,
            pos[1] + diff_y
        )

        if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
            start_cell = data[pos[0]][pos[1]]
            end_cell = data[new_pos[0]][new_pos[1]]

            if start_cell == 'S':
                start_cell = 'a'

            if end_cell == 'E':
                end_cell = 'z'

            if ord(end_cell) - ord(start_cell) <= 1:
                result.append(new_pos)

    return result


def shortest_path(data: List[str]) -> int:
    s_pos = find_pos(data, 'S')
    e_pos = find_pos(data, 'E')
    a_pos_lst = find_all_pos(data, 'a')

    queue = deque([(s_pos, 0)])

    for pos in a_pos_lst:
        queue.append((pos, 0))

    visited = set()
    result = -1

    while len(queue):
        pos, path_len = queue.popleft()
        if pos in visited:
            continue
        if pos == e_pos:
            result = path_len
            break
        visited.add(pos)
        for neighbour in find_neighbours(data, pos):
            queue.append((neighbour, path_len + 1))

    return result


def test_shortest_path():
    data = [
        'Sabqponm',
        'abcryxxl',
        'accszExk',
        'acctuvwj',
        'abdefghi'
    ]

    assert shortest_path(data) == 29


def main():
    data = [line.strip() for line in sys.stdin]
    result = shortest_path(data)
    print(result)


if __name__ == '__main__':
    main()

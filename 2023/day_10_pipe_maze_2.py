#!/usr/bin/env python3

import sys
from collections import deque
from typing import List, Tuple

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

ADJ_DICT = {
    '|': {UP, DOWN},
    '-': {LEFT, RIGHT},
    'L': {UP, RIGHT},
    'J': {UP, LEFT},
    '7': {LEFT, DOWN},
    'F': {RIGHT, DOWN},
}


def resolve_start(data: List[str], start) -> Tuple[Tuple[int, int], str]:
    for i, row in enumerate(data):
        j = row.find(start)
        if j > -1:
            ii, jj = i, j
            break

    dirs = set()

    for i_diff, j_diff in (UP, DOWN, LEFT, RIGHT):
        i, j = ii + i_diff, jj + j_diff
        rev_diff_i, rev_diff_j = -i_diff, -j_diff

        if not (0 <= i < len(data) and 0 <= j < len(data[0])):
            continue

        if (rev_diff_i, rev_diff_j) in ADJ_DICT.get(data[i][j], set()):
            dirs.add((i_diff, j_diff))

    for pipe, adj in ADJ_DICT.items():
        one, two = adj
        if one in dirs and two in dirs:
            break

    return (ii, jj), pipe


def internal_area_size(data: List[str], start='S') -> int:
    start_pos, start_pipe = resolve_start(data, start)

    visited = set(start_pos)
    states = [
        ((start_pos[0] + xx, start_pos[1] + yy), 1)
        for xx, yy in ADJ_DICT[start_pipe]
    ]
    q = deque(states)

    while len(q):
        pos, steps = q.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        x, y = pos
        for x_diff, y_diff in ADJ_DICT.get(data[x][y], set()):
            i, j = x + x_diff, y + y_diff
            if not (0 <= i < len(data) and 0 <= j < len(data[0])):
                continue
            if data[i][j] == '.' or (i, j) in visited:
                continue
            q.append(((i, j), steps + 1))

    for i, row in enumerate(data):
        new_row = list(row)
        for j in range(len(row)):
            if (i, j) in visited:
                new_row[j] = data[i][j] if (i, j) != start_pos else start_pipe
            else:
                new_row[j] = '.'
        data[i] = ''.join(new_row)

    internal_cnt = 0

    for i in range(len(data)):
        for j in range(len(data[0])):
            if is_internal(data, (i, j)):
                internal_cnt += 1

    return internal_cnt


def is_internal(data: List[str], pos: Tuple[int, int]) -> bool:
    x, y = pos
    if data[x][y] != '.':
        return False

    prefix = data[x][:y+1]
    dirs = [adj for item in prefix for adj in ADJ_DICT.get(item, set())]
    status_ups, status_downs = 0, 0

    for adj in dirs:
        if adj == UP:
            status_ups += 1
            status_ups %= 2
        elif adj == DOWN:
            status_downs += 1
            status_downs %= 2

    return status_ups == status_downs == 1


def test_internal_area_size_1():
    data = [
        '...........',
        '.S-------7.',
        '.|F-----7|.',
        '.||.....||.',
        '.||.....||.',
        '.|L-7.F-J|.',
        '.|..|.|..|.',
        '.L--J.L--J.',
        '...........',
    ]
    assert internal_area_size(data) == 4


def test_internal_area_size_2():
    data = [
        '..........',
        '.S------7.',
        '.|F----7|.',
        '.||....||.',
        '.||....||.',
        '.|L-7F-J|.',
        '.|..||..|.',
        '.L--JL--J.',
        '..........',
    ]
    assert internal_area_size(data) == 4


def test_internal_area_size_3():
    data = [
        'FF7FSF7F7F7F7F7F---7',
        'L|LJ||||||||||||F--J',
        'FL-7LJLJ||||||LJL-77',
        'F--JF--7||LJLJ7F7FJ-',
        'L---JF-JLJ.||-FJLJJ7',
        '|F|F-JF---7F7-L7L|7|',
        '|FFJF7L7F-JF7|JL---7',
        '7-L-JL7||F7|L7F-7F7|',
        'L.L7LFJ|||||FJL7||LJ',
        'L7JLJL-JLJLJL--JLJ.L',
    ]
    assert internal_area_size(data) == 10


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = internal_area_size(data)
    print(result)


if __name__ == '__main__':
    main()

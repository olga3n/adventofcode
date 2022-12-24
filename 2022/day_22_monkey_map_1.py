#!/usr/bin/env python3

import sys
from typing import List, Tuple

WALK_DIFFS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}

TURNS = {
    ('>', 'L'): '^',
    ('>', 'R'): 'v',
    ('<', 'L'): 'v',
    ('<', 'R'): '^',
    ('v', 'L'): '>',
    ('v', 'R'): '<',
    ('^', 'L'): '<',
    ('^', 'R'): '>',
}

DIRECTION_SCORE = {
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3
}


def parse_path(raw_path: str) -> List[str]:
    path = []

    curr_number = ''

    for symbol in raw_path:
        if symbol.isdigit():
            curr_number += symbol
        else:
            path.append(curr_number)
            path.append(symbol)
            curr_number = ''

    if curr_number:
        path.append(curr_number)

    return path


def walk(
    field: List[str], pos: Tuple[int, int], direction: str, step: int
) -> Tuple[int, int]:

    diff = WALK_DIFFS[direction]

    for i in range(step):
        row = (pos[0] + diff[0]) % len(field)
        column = (pos[1] + diff[1]) % len(field[row])

        if field[row][column] == '#':
            return pos

        if field[row][column] == '.':
            pos = (row, column)
        elif field[row][column] == ' ':
            new_row, new_column = row, column
            while field[new_row][new_column] == ' ':
                new_row = (new_row + diff[0]) % len(field)
                new_column = (new_column + diff[1]) % len(field[new_row])
            if field[new_row][new_column] == '.':
                pos = (new_row, new_column)

    return pos


def final_pos_score(data: List[str]) -> int:
    field = [line.rstrip() for line in data if len(line.rstrip())]
    field, path = field[:-1], parse_path(field[-1])
    max_row = max(len(line) for line in field)
    field = [line.ljust(max_row, ' ') for line in field]

    pos = (0, field[0].index('.'))

    direction = '>'

    for item in path:
        if item.isdigit():
            pos = walk(field, pos, direction, int(item))
        else:
            direction = TURNS[(direction, item)]

    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + DIRECTION_SCORE[direction]


def test_final_pos_score():
    data = [
        '        ...#',
        '        .#..',
        '        #...',
        '        ....',
        '...#.......#',
        '........#...',
        '..#....#....',
        '..........#.',
        '        ...#....',
        '        .....#..',
        '        .#......',
        '        ......#.',
        '',
        '10R5L5R10L4R5L5'
    ]

    assert final_pos_score(data) == 6032


def main():
    data = sys.stdin.readlines()
    result = final_pos_score(data)
    print(result)


if __name__ == '__main__':
    main()

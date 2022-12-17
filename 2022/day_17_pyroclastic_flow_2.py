#!/usr/bin/env python3

import sys
from typing import List, Tuple, Dict


FIGURES = [
    [
        '..@@@@.',
    ],
    [
        '...@...',
        '..@@@..',
        '...@...',
    ],
    [
        '....@..',
        '....@..',
        '..@@@..',
    ],
    [
        '..@....',
        '..@....',
        '..@....',
        '..@....',
    ],
    [
        '..@@...',
        '..@@...'
    ]
]

ROCKS = list(map(lambda figure: [list(row) for row in figure], FIGURES))

EMPTY_ROWS = [['.'] * 7, ['.'] * 7, ['.'] * 7]


def shift(
    field: List[List[str]], diff: int, figure_char: str = '@'
) -> List[List[str]]:

    new_field = []

    for row in field:
        if figure_char not in row:
            new_field.append(row)
            continue

        new_row = [cell if cell != figure_char else '.' for cell in row]
        ok = True

        for i, char in enumerate(row):
            if char != figure_char:
                continue
            if not 0 <= i + diff < len(row) or new_row[i + diff] != '.':
                ok = False
                break
            new_row[i + diff] = char

        if ok:
            new_field.append(new_row)
        else:
            return field

    return new_field


def fall_down(
    field: List[List[str]], figure_char: str = '@'
) -> Tuple[List[List[str]], bool]:

    new_field = []

    for row_index, row in enumerate(field):
        if row_index != 0 and figure_char not in field[row_index - 1]:
            if figure_char not in row:
                new_field.append(row)
                continue

        new_row = [cell if cell != figure_char else '.' for cell in row]

        if row_index == 0 or figure_char not in field[row_index - 1]:
            new_field.append(new_row)
            continue

        for i, char in enumerate(field[row_index - 1]):
            if char != figure_char:
                continue
            if new_row[i] != '.':
                return field, False
            new_row[i] = char

        new_field.append(new_row)

    for char in field[-1]:
        if char == figure_char:
            return field, False

    return new_field, field != new_field


def clear_empty(field: List[List[str]]) -> List[List[str]]:
    empty_size = 0

    for row in field:
        if all(cell == '.' for cell in row):
            empty_size += 1
        else:
            break

    return field[empty_size:]


def clear_full(field: List[List[str]]) -> Tuple[List[List[str]], int]:
    for row_index, row in enumerate(field):
        if all(cell == '#' for cell in row):
            return field[:row_index], len(field) - row_index
    return field, 0


def replace_fallen(
    field: List[List[str]], from_char: str = '@', to_char: str = '#'
) -> List[List[str]]:
    field = [
        [to_char if cell == from_char else cell for cell in row]
        for row in field
    ]
    return field


def tower_size(rules: str, rocks=1000000000000) -> int:
    field: List[List[str]] = []

    rock = 0
    rock_index = 0
    rule_index = 0

    curr_size = 0

    prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
    diff: Dict[Tuple[int, int], Tuple[int, int]] = {}

    while rock < rocks:
        key = (rock_index, rule_index)

        if key in prev:
            last_rock, last_size = prev[key]
            if key in diff:
                diff_rock = rock - last_rock
                diff_size = curr_size + len(field) - last_size
                if (diff_rock, diff_size) == diff[key]:
                    if rocks - rock >= diff_rock:
                        loops = (rocks - rock) // diff_rock
                        rocks -= loops * diff_rock
                        curr_size += loops * diff_size
                        if rock == rocks:
                            break
            else:
                diff_rock = rock - last_rock
                diff_size = curr_size + len(field) - last_size
                diff[key] = (diff_rock, diff_size)

        prev[key] = (rock, curr_size + len(field))

        field = ROCKS[rock_index].copy() + EMPTY_ROWS.copy() + field

        while True:
            if rules[rule_index] == '>':
                field = shift(field, 1)
            elif rules[rule_index] == '<':
                field = shift(field, -1)

            rule_index += 1
            rule_index %= len(rules)

            field, ok = fall_down(field)

            if not ok:
                break

        field = replace_fallen(field)
        field = clear_empty(field)
        field, size = clear_full(field)
        curr_size += size
        rock += 1
        rock_index = rock % len(ROCKS)

    return curr_size + len(field)


def test_tower_size():
    data = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
    assert tower_size(data) == 1514285714288


def main():
    data = sys.stdin.readline().strip()
    result = tower_size(data)
    print(result)


if __name__ == '__main__':
    main()

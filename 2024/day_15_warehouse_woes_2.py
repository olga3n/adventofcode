#!/usr/bin/env python3

import sys
from typing import Iterable


MOVE_DIFF = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0),
}


def parse_data(lines: Iterable[str]) -> tuple[list[list[str]], list[str]]:
    is_map = True
    table = []
    movements = []
    changes = {
        '.': '..',
        'O': '[]',
        '#': '##',
        '@': '@.',
    }

    for line in lines:
        if len(line) == 0:
            is_map = False
        elif is_map:
            changed_line = ''
            for symbol in line:
                changed_line += changes[symbol]
            table.append(list(changed_line))
        else:
            movements.extend(list(line))

    return table, movements


def full_scan(table: list[list[str]], char: str) -> Iterable[tuple[int, int]]:
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] != char:
                continue
            yield (i, j)


def next_step(
    table: list[list[str]], pos: tuple[int, int], movement: str,
) -> tuple[bool, tuple[int, int]]:
    new_pos = (
        pos[0] + MOVE_DIFF[movement][0],
        pos[1] + MOVE_DIFF[movement][1],
    )

    if not 0 <= new_pos[0] < len(table):
        return False, pos

    if not 0 <= new_pos[1] < len(table[0]):
        return False, pos

    if table[new_pos[0]][new_pos[1]] == '#':
        return False, pos

    return True, new_pos


def shift_hor(
    table: list[list[str]], pos: tuple[int, int], movement: str,
) -> bool:
    lines = []

    if table[pos[0]][pos[1]] == '[':
        left = pos
        right = (left[0], left[1] + 1)
        lines = [[left, right]]
    else:
        right = pos
        left = (right[0], right[1] - 1)
        lines = [[left, right]]

    found_space = False

    curr_pos = pos
    no_space = False

    while not no_space:
        new_line = set()

        for curr_pos in lines[-1]:
            flag, curr_pos = next_step(table, curr_pos, movement)

            if not flag:
                no_space = True
                break

            if table[curr_pos[0]][curr_pos[1]] == '.':
                continue

            new_line.add(curr_pos)

            if table[curr_pos[0]][curr_pos[1]] == '[':
                new_line.add((curr_pos[0], curr_pos[1] + 1))
            elif table[curr_pos[0]][curr_pos[1]] == ']':
                new_line.add((curr_pos[0], curr_pos[1] - 1))

        if no_space:
            break

        if len(new_line) == 0:
            found_space = True
            break

        lines.append(list(new_line))

    if found_space:
        for tiles in reversed(lines):
            for tile in tiles:
                _, shifted = next_step(table, tile, movement)
                table[shifted[0]][shifted[1]] = table[tile[0]][tile[1]]
                table[tile[0]][tile[1]] = '.'

    return found_space


def shift_ver(
    table: list[list[str]], pos: tuple[int, int], movement: str,
) -> bool:
    cols = []
    row = pos[0]

    if table[pos[0]][pos[1]] == '[':
        cols = [pos[1], pos[1] + 1]
    else:
        cols = [pos[1], pos[1] - 1]

    found_space = False

    while True:
        flag, curr_pos = next_step(table, (row, cols[-1]), movement)

        if not flag:
            return False

        if table[curr_pos[0]][curr_pos[1]] == '.':
            found_space = True
            break

        cols.append(curr_pos[1])

    if found_space:
        for c in reversed(cols):
            _, shifted = next_step(table, (row, c), movement)
            table[row][shifted[1]] = table[row][c]
            table[row][c] = '.'

    return found_space


def shift(
    table: list[list[str]], pos: tuple[int, int], movement: str,
) -> bool:
    if movement in {'^', 'v'}:
        return shift_hor(table, pos, movement)
    return shift_ver(table, pos, movement)


def boxes_score(table: list[list[str]], movements: list[str]) -> int:
    robot_pos = next(iter(full_scan(table, '@')))
    table[robot_pos[0]][robot_pos[1]] = '.'

    for movement in movements:
        flag, next_pos = next_step(table, robot_pos, movement)

        if not flag:
            continue

        if table[next_pos[0]][next_pos[1]] in {'[', ']'}:
            if shift(table, next_pos, movement):
                robot_pos = next_pos
        else:
            robot_pos = next_pos

    return sum(i * 100 + j for i, j in full_scan(table, '['))


def test_boxes_score():
    lines = [
        '##########',
        '#..O..O.O#',
        '#......O.#',
        '#.OO..O.O#',
        '#..O@..O.#',
        '#O#..O...#',
        '#O..O..O.#',
        '#.OO.O.OO#',
        '#....O...#',
        '##########',
        '',
        '<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^',
        'vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v',
        '><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<',
        '<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^',
        '^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><',
        '^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^',
        '>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^',
        '<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>',
        '^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>',
        'v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^',
    ]
    assert 9021 == boxes_score(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = boxes_score(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()

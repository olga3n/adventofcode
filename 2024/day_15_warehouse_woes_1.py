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

    for line in lines:
        if len(line) == 0:
            is_map = False
        elif is_map:
            table.append(list(line))
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


def shift(
    table: list[list[str]], pos: tuple[int, int], movement: str,
) -> bool:
    curr_pos = pos

    while True:
        flag, curr_pos = next_step(table, curr_pos, movement)

        if not flag:
            break

        if table[curr_pos[0]][curr_pos[1]] == '.':
            table[curr_pos[0]][curr_pos[1]] = 'O'
            table[pos[0]][pos[1]] = '.'
            return True

    return False


def boxes_score(table: list[list[str]], movements: list[str]) -> int:
    robot_pos = next(iter(full_scan(table, '@')))
    table[robot_pos[0]][robot_pos[1]] = '.'

    for movement in movements:
        flag, next_pos = next_step(table, robot_pos, movement)

        if not flag:
            continue

        if table[next_pos[0]][next_pos[1]] == 'O':
            if shift(table, next_pos, movement):
                robot_pos = next_pos
        else:
            robot_pos = next_pos

    return sum(i * 100 + j for i, j in full_scan(table, 'O'))


def test_boxes_score_0():
    lines = [
        '########',
        '#..O.O.#',
        '##@.O..#',
        '#...O..#',
        '#.#.O..#',
        '#...O..#',
        '#......#',
        '########',
        '',
        '<^^>>>vv<v>>v<<',
    ]
    assert 2028 == boxes_score(*parse_data(lines))


def test_boxes_score_1():
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
    assert 10092 == boxes_score(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = boxes_score(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()

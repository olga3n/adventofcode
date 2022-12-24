#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class Rule:
    check: Tuple[Tuple[int, int], ...]
    move: Tuple[int, int]


def build_movements(
    field: List[List[str]], rules: List[Rule]
) -> Dict[Tuple[int, int], Tuple[int, int]]:
    movements = {}

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != '#':
                continue

            flag = False

            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == dj == 0:
                        continue
                    if not 0 <= i + di < len(field):
                        continue
                    if not 0 <= j + dj < len(field[i + di]):
                        continue
                    if field[i + di][j + dj] == '#':
                        flag = True
                        break
                if flag:
                    break

            if not flag:
                movements[(i, j)] = (i, j)
                continue

            flag = False

            for rule in rules:
                gen = (
                    field[i + di][j + dj] == '.' for di, dj in rule.check
                )
                if all(gen):
                    flag = True
                    movements[(i, j)] = (
                        i + rule.move[0],
                        j + rule.move[1]
                    )
                    break

            if not flag:
                movements[(i, j)] = (i, j)

    return movements


def extend_field(field: List[List[str]]) -> List[List[str]]:
    if '#' in field[0]:
        field = [['.'] * len(field[0])] + field
    if '#' in field[-1]:
        field = field + [['.'] * len(field[-1])]
    if '#' in (row[0] for row in field):
        field = [['.'] + row for row in field]
    if '#' in (row[-1] for row in field):
        field = [row + ['.'] for row in field]
    return field


def elves_movements_score(data: List[str], steps: int = 10) -> int:
    field = [list(line.rstrip()) for line in data]
    field = extend_field(field)

    rules = [
        Rule(check=((-1, 0), (-1, -1), (-1, 1)), move=(-1, 0)),
        Rule(check=((1, 0), (1, -1), (1, 1)), move=(1, 0)),
        Rule(check=((0, -1), (-1, -1), (1, -1)), move=(0, -1)),
        Rule(check=((0, 1), (-1, 1), (1, 1)), move=(0, 1))
    ]

    for step in range(steps):
        movements = build_movements(field, rules)

        inv_movements = {}

        for k, v in movements.items():
            if v not in inv_movements:
                inv_movements[v] = [k]
            else:
                inv_movements[v].append(k)

        final_movements = {}

        for k, lst_v in inv_movements.items():
            if len(lst_v) == 1:
                final_movements[k] = lst_v[0]
            else:
                for item in lst_v:
                    final_movements[item] = item

        new_field = []

        for i in range(len(field)):
            row = [
                '#' if (i, j) in final_movements else '.'
                for j in range(len(field[i]))
            ]
            new_field.append(row)

        field = extend_field(new_field)
        rules = rules[1:] + rules[:1]

    min_row = 0
    max_row = len(field) - 1

    while '#' not in field[min_row]:
        min_row += 1

    while '#' not in field[max_row]:
        max_row -= 1

    min_column = 0
    max_column = len(field[0]) - 1

    while '#' not in (line[min_column] for line in field):
        min_column += 1

    while '#' not in (line[max_column] for line in field):
        max_column -= 1

    result = sum(
        1 for row in range(min_row, max_row + 1)
        for column in range(min_column, max_column + 1)
        if field[row][column] == '.'
    )

    return result


def test_elves_movements_score():
    data = [
        '..............',
        '..............',
        '.......#......',
        '.....###.#....',
        '...#...#.#....',
        '....#...##....',
        '...#.###......',
        '...##.#.##....',
        '....#..#......',
        '..............',
        '..............',
        '..............'
    ]

    assert elves_movements_score(data) == 110


def main():
    data = sys.stdin.readlines()
    result = elves_movements_score(data)
    print(result)


if __name__ == '__main__':
    main()

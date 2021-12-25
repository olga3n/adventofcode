#!/usr/bin/env python3

import sys
from typing import List, Tuple


def make_step(table: List[List[str]]) -> Tuple[int, List[List[str]]]:
    result = 0
    new_table = []

    for i in range(len(table)):
        new_row = table[i].copy()
        for j in range(len(table[i])):
            jj = (j + 1) % len(table[i])
            if table[i][j] == '>' and table[i][jj] == '.':
                new_row[j] = '.'
                new_row[jj] = '>'
                result += 1
        new_table.append(new_row)

    table = new_table
    new_table = [row.copy() for row in table]

    for i in range(len(table)):
        for j in range(len(table[i])):
            ii = (i + 1) % len(table)
            if table[i][j] == 'v' and table[ii][j] == '.':
                new_table[i][j] = '.'
                new_table[ii][j] = 'v'
                result += 1

    return result, new_table


def process_steps(data: List[str]):
    table = [list(row) for row in data]
    step = 0

    while True:
        movements, table = make_step(table)
        step += 1
        if movements == 0:
            break

    return step


class TestClass():

    def test_1(self):
        data = [
            'v...>>.vv>',
            '.vv>>.vv..',
            '>>.>v>...v',
            '>>v>>.>.v.',
            'v>v.vv.v..',
            '>.>>..v...',
            '.vv..>.>v.',
            'v.v..>>v.v',
            '....v..v.>',
        ]
        assert process_steps(data) == 58


def main():
    data = [x.strip('\n') for x in sys.stdin]
    result = process_steps(data)
    print(result)


if __name__ == '__main__':
    main()

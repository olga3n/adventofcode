#!/usr/bin/env python3

import sys
from typing import Iterable, List, Tuple


def get_neighbours(
    rows: int, cols: int, pos: Tuple[int, int]
) -> Iterable[Tuple[int, int]]:
    for dx in (-1, 0, 1):
        if not 0 <= pos[0] + dx < rows:
            continue
        for dy in (-1, 0, 1):
            if not 0 <= pos[1] + dy < cols:
                continue
            if dx == dy == 0:
                continue
            yield (pos[0] + dx, pos[1] + dy)


def is_symbol(ch: str) -> bool:
    if '0' <= ch <= '9':
        return False
    if ch == '.':
        return False
    return True


def check_neighbours(
    data: List[str], positions: List[Tuple[int, int]]
) -> bool:
    rows, cols = len(data), len(data[0])
    return any(
        is_symbol(data[x][y]) for pos in positions
        for x, y in get_neighbours(rows, cols, pos)
    )


def sum_numbers(data: List[str]):
    numbers = []

    for i in range(len(data)):
        j, number, positions = 0, '', []
        while j < len(data[i]):
            if '0' <= data[i][j] <= '9':
                number += data[i][j]
                positions.append((i, j))
            if j == len(data[i]) - 1 or not '0' <= data[i][j] <= '9':
                if number and check_neighbours(data, positions):
                    numbers.append(int(number))
                number, positions = '', []
            j += 1

    return sum(numbers)


def test_sum_numbers():
    data = [
        '467..114..',
        '...*......',
        '..35..633.',
        '......#...',
        '617*......',
        '.....+.58.',
        '..592.....',
        '......755.',
        '...$.*....',
        '.664.598..',
    ]
    assert sum_numbers(data) == 4361


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = sum_numbers(data)
    print(result)


if __name__ == '__main__':
    main()

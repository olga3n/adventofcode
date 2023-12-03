#!/usr/bin/env python3

import sys
from typing import Any, Dict, Iterable, List, Set, Tuple


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


def gear_neighbours(
    data: List[str], positions: List[Tuple[int, int]]
) -> Set[Tuple[int, int]]:
    rows, cols = len(data), len(data[0])
    return set(
        (x, y) for pos in positions
        for x, y in get_neighbours(rows, cols, pos)
        if data[x][y] == '*'
    )


def find_numbers(
    data: List[str]
) -> Dict[Tuple[int, int, int], Set[Tuple[int, int]]]:
    result = {}
    for i in range(len(data)):
        j, number, positions = 0, '', []
        while j < len(data[i]):
            if '0' <= data[i][j] <= '9':
                number += data[i][j]
                positions.append((i, j))
            if j == len(data[i]) - 1 or not '0' <= data[i][j] <= '9':
                if number:
                    gears = gear_neighbours(data, positions)
                    if gears:
                        jj = j if j == len(data[i]) - 1 else j - 1
                        result[(int(number), i, jj)] = gears
                number, positions = '', []
            j += 1
    return result


def invert_dict(source_dict: Dict[Any, Set[Any]]) -> Dict[Any, Set[Any]]:
    result = {}
    for key, value in source_dict.items():
        for item in value:
            if item not in result:
                result[item] = {key}
            else:
                result[item].add(key)
    return result


def sum_gear_ratios(data: List[str]):
    numbers_dict = find_numbers(data)
    gear_dict = invert_dict(numbers_dict)
    gear_numbers = (
        tuple(number[0] for number in numbers)
        for numbers in gear_dict.values()
        if len(numbers) == 2
    )
    return sum(x * y for x, y in gear_numbers)


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
    assert sum_gear_ratios(data) == 467835


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = sum_gear_ratios(data)
    print(result)


if __name__ == '__main__':
    main()

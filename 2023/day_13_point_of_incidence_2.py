#!/usr/bin/env python3

import sys
from typing import List, Iterable


def parse_patterns(data: Iterable) -> Iterable[List[str]]:
    pattern = []

    for line in data:
        if len(line) == 0:
            yield pattern
            pattern = []
        else:
            pattern.append(line)

    if pattern:
        yield pattern


def find_second_vertical_mirror(pattern: List[str]) -> int:
    for shift in range(1, len(pattern[0])):
        ok = True
        total_errors = 0
        for row in pattern:
            left_seq = (row[i] for i in range(shift - 1, -1, -1))
            right_seq = (row[i] for i in range(shift, len(row)))
            total_errors += sum(
                1 for x, y in zip(left_seq, right_seq) if x != y
            )
            if total_errors > 1:
                ok = False
                break
        if ok and total_errors == 1:
            return shift
    return -1


def rotate_pattern(pattern: List[str]) -> List[str]:
    new_pattern = [
        ''.join([pattern[j][i] for j in range(len(pattern))])
        for i in range(len(pattern[0]))
    ]
    return new_pattern


def mirror_score(pattern: List[str]) -> int:
    vertical = find_second_vertical_mirror(pattern)
    if vertical > 0:
        return vertical
    pattern = rotate_pattern(pattern)
    return 100 * find_second_vertical_mirror(pattern)


def total_mirror_score(data: Iterable[str]) -> int:
    return sum(mirror_score(pattern) for pattern in parse_patterns(data))


def test_total_mirror_score():
    data = [
        '#.##..##.',
        '..#.##.#.',
        '##......#',
        '##......#',
        '..#.##.#.',
        '..##..##.',
        '#.#.##.#.',
        '',
        '#...##..#',
        '#....#..#',
        '..##..###',
        '#####.##.',
        '#####.##.',
        '..##..###',
        '#....#..#',
    ]
    assert total_mirror_score(data) == 400


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = total_mirror_score(data)
    print(result)


if __name__ == '__main__':
    main()

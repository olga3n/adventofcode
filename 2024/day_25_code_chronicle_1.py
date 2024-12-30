#!/usr/bin/env python3

import sys
from typing import Iterable


def pattern_depth(pattern: list[str]) -> tuple[int, ...]:
    buf = [0] * len(pattern[0])

    for i in range(len(buf)):
        for row in range(len(pattern)):
            if pattern[row][i] == '#':
                buf[i] += 1

    return tuple([x - 1 for x in buf])


def parse_data(
    lines: Iterable[str],
) -> tuple[set[tuple[int, ...]], set[tuple[int, ...]]]:
    keys = set()
    locks = set()
    pattern = []

    for line in lines:
        if len(line):
            pattern.append(line)
        elif pattern:
            if pattern[0][0] == '.':
                keys.add(pattern_depth(pattern))
            else:
                locks.add(pattern_depth(pattern))
            pattern = []

    if pattern:
        if pattern[0][0] == '.':
            keys.add(pattern_depth(pattern))
        else:
            locks.add(pattern_depth(pattern))

    return keys, locks


def key_lock_pairs(
    keys: set[tuple[int, ...]], locks: set[tuple[int, ...]], max_size: int = 5,
) -> int:
    result = 0

    for key in keys:
        for lock in locks:
            is_ok = True

            for i in range(len(lock)):
                if key[i] + lock[i] > max_size:
                    is_ok = False
                    break

            if is_ok:
                result += 1

    return result


def test_key_lock_pairs():
    lines = [
        '#####',
        '.####',
        '.####',
        '.####',
        '.#.#.',
        '.#...',
        '.....',
        '',
        '#####',
        '##.##',
        '.#.##',
        '...##',
        '...#.',
        '...#.',
        '.....',
        '',
        '.....',
        '#....',
        '#....',
        '#...#',
        '#.#.#',
        '#.###',
        '#####',
        '',
        '.....',
        '.....',
        '#.#..',
        '###..',
        '###.#',
        '###.#',
        '#####',
        '',
        '.....',
        '.....',
        '.....',
        '#....',
        '#.#..',
        '#.#.#',
        '#####',
    ]
    assert 3 == key_lock_pairs(*parse_data(lines))


def main():
    lines = (line.rstrip() for line in sys.stdin)
    result = key_lock_pairs(*parse_data(lines))
    print(result)


if __name__ == '__main__':
    main()

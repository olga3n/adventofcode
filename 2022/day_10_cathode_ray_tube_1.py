#!/usr/bin/env python3

import sys
from typing import Iterable


def signal_strength(
    data: Iterable[str], first_cycle: int = 20, step: int = 40
) -> int:
    data_iter = (
        (2, int(line.rstrip().split()[-1]))
        if line.startswith("addx") else (1, 0)
        for line in data
    )

    register = 1
    cycle = 1
    result = 0

    size, value = next(data_iter, (0, 0))

    while True:
        if cycle >= first_cycle and (cycle - first_cycle) % step == 0:
            strength = cycle * register
            result += strength

        cycle += 1
        size -= 1

        if size < 0:
            break

        if size == 0:
            register += value
            size, value = next(data_iter, (0, 0))

    return result


def test_signal_strength():
    data = [
        'addx 15',
        'addx -11',
        'addx 6',
        'addx -3',
        'addx 5',
        'addx -1',
        'addx -8',
        'addx 13',
        'addx 4',
        'noop',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx 5',
        'addx -1',
        'addx -35',
        'addx 1',
        'addx 24',
        'addx -19',
        'addx 1',
        'addx 16',
        'addx -11',
        'noop',
        'noop',
        'addx 21',
        'addx -15',
        'noop',
        'noop',
        'addx -3',
        'addx 9',
        'addx 1',
        'addx -3',
        'addx 8',
        'addx 1',
        'addx 5',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx -36',
        'noop',
        'addx 1',
        'addx 7',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'addx 6',
        'noop',
        'noop',
        'noop',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx 7',
        'addx 1',
        'noop',
        'addx -13',
        'addx 13',
        'addx 7',
        'noop',
        'addx 1',
        'addx -33',
        'noop',
        'noop',
        'noop',
        'addx 2',
        'noop',
        'noop',
        'noop',
        'addx 8',
        'noop',
        'addx -1',
        'addx 2',
        'addx 1',
        'noop',
        'addx 17',
        'addx -9',
        'addx 1',
        'addx 1',
        'addx -3',
        'addx 11',
        'noop',
        'noop',
        'addx 1',
        'noop',
        'addx 1',
        'noop',
        'noop',
        'addx -13',
        'addx -19',
        'addx 1',
        'addx 3',
        'addx 26',
        'addx -30',
        'addx 12',
        'addx -1',
        'addx 3',
        'addx 1',
        'noop',
        'noop',
        'noop',
        'addx -9',
        'addx 18',
        'addx 1',
        'addx 2',
        'noop',
        'noop',
        'addx 9',
        'noop',
        'noop',
        'noop',
        'addx -1',
        'addx 2',
        'addx -37',
        'addx 1',
        'addx 3',
        'noop',
        'addx 15',
        'addx -21',
        'addx 22',
        'addx -6',
        'addx 1',
        'noop',
        'addx 2',
        'addx 1',
        'noop',
        'addx -10',
        'noop',
        'noop',
        'addx 20',
        'addx 1',
        'addx 2',
        'addx 2',
        'addx -6',
        'addx -11',
        'noop',
        'noop',
        'noop'
    ]

    assert signal_strength(data) == 13140


def main():
    data = sys.stdin
    result = signal_strength(data)
    print(result)


if __name__ == '__main__':
    main()

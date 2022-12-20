#!/usr/bin/env python3

import sys
from typing import List, Tuple


def mix_process(numbers: List[int]) -> List[int]:
    pairs = list(zip(range(len(numbers)), numbers))

    for i in range(len(pairs)):
        value = numbers[i]
        if value % len(numbers) == 0:
            continue
        index = pairs.index((i, value))
        rest = pairs[index + 1:] + pairs[:index]
        if value > 0:
            shift = value % (len(numbers) - 1)
            pairs = rest[:shift] + [pairs[index]] + rest[shift:]
        elif value < 0:
            shift = abs(value) % (len(numbers) - 1)
            pairs = rest[:-shift] + [pairs[index]] + rest[-shift:]

    return [x[1] for x in pairs]


def mix_score(
    data: List[str], start_value: int = 0,
    ids: Tuple[int, ...] = (1000, 2000, 3000)
) -> int:
    numbers = [int(x) for x in data]
    mixed_data = mix_process(numbers)
    start_index = mixed_data.index(start_value)
    mixed_data = mixed_data[start_index:] + mixed_data[:start_index]
    return sum(mixed_data[index % len(mixed_data)] for index in ids)


def test_mix_score():
    data = [
        '1',
        '2',
        '-3',
        '3',
        '-2',
        '0',
        '4'
    ]

    assert mix_score(data) == 3


def main():
    data = sys.stdin.readlines()
    result = mix_score(data)
    print(result)


if __name__ == '__main__':
    main()

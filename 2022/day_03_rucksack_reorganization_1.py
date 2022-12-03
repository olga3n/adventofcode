#!/usr/bin/env python3

import sys
from typing import Iterable


def rucksack_score(data: Iterable[str]) -> int:
    result = 0

    for line in data:
        half = len(line) // 2
        item = set(line[:half]).intersection(set(line[half:])).pop()
        if item.islower():
            code = ord(item) - ord('a') + 1
        else:
            code = ord(item) - ord('A') + 27
        result += code

    return result


def test_rucksack_score():
    data = [
        'vJrwpWtwJgWrhcsFMMfFFhFp',
        'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL',
        'PmmdzqPrVvPwwTWBwg',
        'wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn',
        'ttgJtRGJQctTZtZT',
        'CrZsJsPPZsGzwwsLwLmpwMDw'
    ]

    assert rucksack_score(data) == 157


def main():
    data = (x.strip() for x in sys.stdin)
    result = rucksack_score(data)
    print(result)


if __name__ == '__main__':
    main()

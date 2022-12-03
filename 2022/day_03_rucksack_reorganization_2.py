#!/usr/bin/env python3

import sys
from functools import reduce
from typing import Iterable, Set


def build_groups(
    data: Iterable[str], batch_size=3
) -> Iterable[Iterable[Set[str]]]:
    batch = []

    for line in data:
        batch.append(set(line))
        if len(batch) == 3:
            yield batch
            batch = []


def rucksack_score(data: Iterable[str]) -> int:
    result = 0

    for batch in build_groups(data):
        item = reduce(lambda x, y: x.intersection(y), batch).pop()
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

    assert rucksack_score(data) == 70


def main():
    data = (x.strip() for x in sys.stdin)
    result = rucksack_score(data)
    print(result)


if __name__ == '__main__':
    main()

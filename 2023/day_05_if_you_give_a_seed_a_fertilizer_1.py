#!/usr/bin/env python3

import sys
from copy import copy
from typing import Iterable, Tuple, List
from dataclasses import dataclass


@dataclass
class MapItem:
    source_start: int
    source_end: int
    dest_diff: int

    @classmethod
    def from_string(cls, line: str):
        dest_start, source_start, range_len = list(map(int, line.split()))
        return cls(
            source_start,
            source_start + range_len - 1,
            dest_start - source_start
        )


def parse_data(data: Iterable[str]) -> Tuple[List[List[MapItem]], List[int]]:
    steps, maps, seeds = [], [], []
    for index, line in enumerate(data):
        if index == 0:
            seeds = list(map(int, line.split(': ')[1].split()))
            continue
        if (len(line) == 0 or line[-1] == ':'):
            if maps:
                steps.append(maps)
                maps = []
        else:
            maps.append(MapItem.from_string(line))
    if maps:
        steps.append(maps)
    return steps, seeds


def locations(data: Iterable[str]) -> List[int]:
    steps, seeds = parse_data(data)
    for maps in steps:
        new_seeds = copy(seeds)
        for map_item in maps:
            for i in range(len(seeds)):
                if map_item.source_start <= seeds[i] <= map_item.source_end:
                    new_seeds[i] += map_item.dest_diff
        seeds = new_seeds
    return seeds


def lowest_location(data: Iterable[str]) -> int:
    return min(locations(data))


def test_lowest_location():
    data = [
        'seeds: 79 14 55 13',
        '',
        'seed-to-soil map:',
        '50 98 2',
        '52 50 48',
        '',
        'soil-to-fertilizer map:',
        '0 15 37',
        '37 52 2',
        '39 0 15',
        '',
        'fertilizer-to-water map:',
        '49 53 8',
        '0 11 42',
        '42 0 7',
        '57 7 4',
        '',
        'water-to-light map:',
        '88 18 7',
        '18 25 70',
        '',
        'light-to-temperature map:',
        '45 77 23',
        '81 45 19',
        '68 64 13',
        '',
        'temperature-to-humidity map:',
        '0 69 1',
        '1 0 69',
        '',
        'humidity-to-location map:',
        '60 56 37',
        '56 93 4',
    ]
    assert lowest_location(data) == 35


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = lowest_location(data)
    print(result)


if __name__ == '__main__':
    main()

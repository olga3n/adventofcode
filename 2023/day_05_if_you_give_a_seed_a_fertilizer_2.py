#!/usr/bin/env python3

import sys
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


@dataclass
class Segment:
    start: int
    end: int


def parse_data(
    data: Iterable[str]
) -> Tuple[List[List[MapItem]], List[Segment]]:
    steps, maps, seeds = [], [], []

    for index, line in enumerate(data):
        if index == 0:
            values = list(map(int, line.split(': ')[1].split()))
            seeds = [
                Segment(values[i], values[i] + values[i + 1] - 1)
                for i in range(0, len(values), 2)
            ]
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


def cut_parts(segment: Segment, map_item: MapItem) -> List[Segment]:
    one = map_item.source_start <= segment.start <= map_item.source_end
    two = map_item.source_start <= segment.end <= map_item.source_end

    if not one and not two:
        return [segment]

    intersection = Segment(
        max(segment.start, map_item.source_start),
        min(segment.end, map_item.source_end)
    )

    parts = [intersection]

    if segment.start < intersection.start:
        parts.append(Segment(segment.start, intersection.start - 1))

    if segment.end > intersection.end:
        parts.append(Segment(intersection.end + 1, segment.end))

    return parts


def locations(data: Iterable[str]) -> List[Segment]:
    steps, seeds = parse_data(data)

    for maps in steps:
        for map_item in maps:
            new_seeds = []
            for segment in seeds:
                new_seeds += cut_parts(segment, map_item)
            seeds = new_seeds

        new_seeds = []

        for segment in seeds:
            for map_item in maps:
                one = map_item.source_start <= segment.start
                two = segment.end <= map_item.source_end
                if one and two:
                    segment = Segment(
                        segment.start + map_item.dest_diff,
                        segment.end + map_item.dest_diff
                    )
                    break

            new_seeds.append(segment)

        seeds = new_seeds

    return seeds


def lowest_location(data: Iterable[str]) -> int:
    return min(item.start for item in locations(data))


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
    assert lowest_location(data) == 46


def main():
    data = (line.rstrip() for line in sys.stdin)
    result = lowest_location(data)
    print(result)


if __name__ == '__main__':
    main()

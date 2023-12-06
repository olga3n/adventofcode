#!/usr/bin/env python3

import sys
from typing import List
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def parse_races(data: List[str]) -> List[Race]:
    values = [data[i].split(':')[1].split() for i in range(2)]
    values = [list(map(int, row)) for row in values]
    return [Race(values[0][i], values[1][i]) for i in range(len(values[0]))]


def race_total_win_ways(race: Race) -> int:
    max_ways = 0

    for hold in range(race.time + 1):
        if hold == 0 or hold == race.time:
            distance = 0
        else:
            distance = (race.time - hold) * hold

        if distance > race.distance:
            max_ways += 1

    return max_ways


def total_win_ways_score(data: List[str]) -> int:
    value = 1
    for race in parse_races(data):
        value *= race_total_win_ways(race)
    return value


def test_total_win_ways_score():
    data = [
        'Time:      7  15   30',
        'Distance:  9  40  200',
    ]
    assert total_win_ways_score(data) == 288


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = total_win_ways_score(data)
    print(result)


if __name__ == '__main__':
    main()

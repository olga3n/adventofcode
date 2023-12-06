#!/usr/bin/env python3

import sys
from typing import List
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def parse_race(data: List[str]) -> Race:
    values = [data[i].split(':')[1] for i in range(2)]
    values = [int(''.join(ch for ch in row if ch != ' ')) for row in values]
    return Race(values[0], values[1])


def race_total_win_ways(race: Race) -> int:
    min_hold, max_hold = 0, -1

    for hold in range(race.time + 1):
        if hold == 0 or hold == race.time:
            distance = 0
        else:
            distance = (race.time - hold) * hold

        if distance > race.distance:
            min_hold = hold
            break

    for hold in range(race.time + 1, -1, -1):
        if hold == 0 or hold == race.time:
            distance = 0
        else:
            distance = (race.time - hold) * hold

        if distance > race.distance:
            max_hold = hold
            break

    return max_hold - min_hold + 1


def total_win_ways_score(data: List[str]) -> int:
    return race_total_win_ways(parse_race(data))


def test_total_win_ways_score():
    data = [
        'Time:      7  15   30',
        'Distance:  9  40  200',
    ]
    assert total_win_ways_score(data) == 71503


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = total_win_ways_score(data)
    print(result)


if __name__ == '__main__':
    main()

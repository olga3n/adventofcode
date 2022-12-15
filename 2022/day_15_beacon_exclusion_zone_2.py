#!/usr/bin/env python3

import sys
import re
from typing import Iterable


def tuning_freq(
    data: Iterable[str], min_coordinate: int = 0, max_coordinate: int = 4000000
) -> int:
    coordinates_s = []
    rows = set()
    pos = (0, 0)

    for line in data:
        s_x, s_y, b_x, b_y = map(int, re.findall(r'-?\d+', line))
        dist = abs(s_x - b_x) + abs(s_y - b_y)
        coordinates_s.append((s_x, s_y, dist))

        if 0 <= s_y <= max_coordinate:
            rows.add(s_y)

        if 0 <= b_y <= max_coordinate:
            rows.add(s_x)

    for row in range(min_coordinate, max_coordinate + 1):
        intervals = []

        for s_x, s_y, dist in coordinates_s:
            dy = abs(s_y - row)
            dx = dist - dy
            if dx >= 0:
                min_x, max_x = s_x - dx, s_x + dx
                intervals.append((min_x, max_x))

        joined_intervals = []
        intervals.sort()

        start, end = intervals[0]

        for i in range(1, len(intervals)):
            seg_start, seg_end = intervals[i]
            if end + 1 == seg_start:
                end = max(end, seg_end)
            elif max(start, seg_start) <= min(end, seg_end):
                end = max(end, seg_end)
            else:
                joined_intervals.append((start, end))
                start, end = seg_start, seg_end

        joined_intervals.append((start, end))

        if len(joined_intervals) == 2:
            if joined_intervals[1][0] - joined_intervals[0][1] == 2:
                pos = (joined_intervals[0][1] + 1, row)
                break

    return 4000000 * pos[0] + pos[1]


def test_tuning_freq():
    data = [
        'Sensor at x=2, y=18: closest beacon is at x=-2, y=15',
        'Sensor at x=9, y=16: closest beacon is at x=10, y=16',
        'Sensor at x=13, y=2: closest beacon is at x=15, y=3',
        'Sensor at x=12, y=14: closest beacon is at x=10, y=16',
        'Sensor at x=10, y=20: closest beacon is at x=10, y=16',
        'Sensor at x=14, y=17: closest beacon is at x=10, y=16',
        'Sensor at x=8, y=7: closest beacon is at x=2, y=10',
        'Sensor at x=2, y=0: closest beacon is at x=2, y=10',
        'Sensor at x=0, y=11: closest beacon is at x=2, y=10',
        'Sensor at x=20, y=14: closest beacon is at x=25, y=17',
        'Sensor at x=17, y=20: closest beacon is at x=21, y=22',
        'Sensor at x=16, y=7: closest beacon is at x=15, y=3',
        'Sensor at x=14, y=3: closest beacon is at x=15, y=3',
        'Sensor at x=20, y=1: closest beacon is at x=15, y=3'
    ]

    assert tuning_freq(data, max_coordinate=20) == 56000011


def main():
    data = sys.stdin
    result = tuning_freq(data)
    print(result)


if __name__ == '__main__':
    main()

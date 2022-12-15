#!/usr/bin/env python3

import sys
import re
from typing import Iterable, List, Tuple


def join_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
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
    return joined_intervals


def free_positions(data: Iterable[str], row: int = 2000000) -> int:
    intervals = []
    exclude = set()

    for line in data:
        s_x, s_y, b_x, b_y = map(int, re.findall(r'-?\d+', line))

        if s_y == row:
            exclude.add(s_x)

        if b_y == row:
            exclude.add(b_x)

        dist = abs(s_x - b_x) + abs(s_y - b_y)
        dy = abs(s_y - row)
        dx = dist - dy

        if dx >= 0:
            min_x, max_x = s_x - dx, s_x + dx
            intervals.append((min_x, max_x))

    joined_intervals = join_intervals(intervals)
    intervals_size = sum(end - start + 1 for start, end in joined_intervals)

    return intervals_size - len(exclude)


def test_free_positions():
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

    assert free_positions(data, row=10) == 26


def main():
    data = sys.stdin
    result = free_positions(data)
    print(result)


if __name__ == '__main__':
    main()

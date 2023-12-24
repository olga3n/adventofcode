#!/usr/bin/env python3

import sys
from typing import Iterable, Tuple


def parse_data(
    data: Iterable[str]
) -> Iterable[Tuple[Tuple[int, ...], Tuple[int, ...]]]:
    for line in data:
        left, right = line.split(' @ ')
        left = tuple(map(int, left.split(', ')))
        right = tuple(map(int, right.split(', ')))
        yield (left, right)


def check_intersection(
    start_1: Tuple[int, int, int], velocity_1: Tuple[int, int, int],
    start_2: Tuple[int, int, int], velocity_2: Tuple[int, int, int]
) -> bool:
    if velocity_1[0] != velocity_2[0]:
        t = (start_2[0] - start_1[0]) / (velocity_1[0] - velocity_2[0])
        point_1 = (
            start_1[0] + t * velocity_1[0],
            start_1[1] + t * velocity_1[1],
            start_1[2] + t * velocity_1[2]
        )
        point_2 = (
            start_2[0] + t * velocity_2[0],
            start_2[1] + t * velocity_2[1],
            start_2[2] + t * velocity_2[2]
        )
        if point_1 == point_2:
            return True

    return False


def check_candidate(lines, start, velocity) -> bool:
    for line in lines:
        if not check_intersection(line[0], line[1], start, velocity):
            return False
    return True


def rock_score(data: Iterable[str]) -> int:
    lines = list(parse_data(data))

    x0, y0, z0 = lines[0][0]
    x1, y1, z1 = lines[1][0]

    vx0, vy0, vz0 = lines[0][1]
    vx1, vy1, vz1 = lines[1][1]

    limit = max(max(max(line[1]), -min(line[1])) for line in lines)
    min_v, max_v = -limit, limit

    print('check velocity in range:', (min_v, max_v), file=sys.stderr)

    for vxr in range(min_v, max_v + 1):
        print(f'check velocity ({vxr}, xx, xx)', file=sys.stderr)

        for vyr in range(min_v, max_v + 1):
            for vzr in range(min_v, max_v + 1):
                coeff_1 = (vx1 - vxr) * (vy0 - vyr) - (vy1 - vyr) * (vx0 - vxr)
                if coeff_1 == 0:
                    continue

                t1 = (
                    (y1 - y0) * (vx0 - vxr) - (x1 - x0) * (vy0 - vyr)
                ) / coeff_1

                coeff_0 = vx0 - vxr
                if coeff_0 == 0:
                    continue

                t0 = (t1 * (vx1 - vxr) + x1 - x0) / coeff_0
                if t0 * (vz0 - vzr) + z0 != t1 * (vz1 - vzr) + z1:
                    continue

                velocity = (vxr, vyr, vzr)

                print('found velocity:', velocity, file=sys.stderr)

                xr = x0 + int(t0) * (vx0 - vxr)
                yr = y0 + int(t0) * (vy0 - vyr)
                zr = z0 + int(t0) * (vz0 - vzr)

                rock = (xr, yr, zr)

                if not all(
                    check_intersection(line[0], line[1], rock, velocity)
                    for line in lines
                ):
                    continue

                print('found rock:', rock, file=sys.stderr)

                return sum(rock)


def test_rock_score():
    data = [
        '19, 13, 30 @ -2,  1, -2',
        '18, 19, 22 @ -1, -1, -2',
        '20, 25, 34 @ -2, -2, -4',
        '12, 31, 28 @ -1, -2, -1',
        '20, 19, 15 @  1, -5, -3',
    ]
    assert rock_score(data) == 47


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = rock_score(data)
    print(result)


if __name__ == '__main__':
    main()

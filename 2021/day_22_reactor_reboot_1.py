#!/usr/bin/env python3

import sys
import re
from typing import List


def cube_status(
    data: List[str], min_limit: int = -50, max_limit: int = 50
) -> int:

    x_borders_set = {min_limit, max_limit + 1}
    y_borders_set = {min_limit, max_limit + 1}
    z_borders_set = {min_limit, max_limit + 1}

    records = []

    for line in data:
        status = 1 if line.startswith('on') else 0
        positions = list(map(int, re.findall(r"-?\d+", line)))

        x_borders_set.add(positions[0])
        x_borders_set.add(positions[1] + 1)

        y_borders_set.add(positions[2])
        y_borders_set.add(positions[3] + 1)

        z_borders_set.add(positions[4])
        z_borders_set.add(positions[5] + 1)

        records.append((status, positions))

    statuses = []

    x_borders = sorted(x_borders_set)
    y_borders = sorted(y_borders_set)
    z_borders = sorted(z_borders_set)

    for item_x in x_borders:
        lst = []
        for item_y in y_borders:
            lst.append([0] * len(z_borders))
        statuses.append(lst)

    for status, position in records:
        x0, x1, y0, y1, z0, z1 = position
        for i, x_border in enumerate(x_borders):
            if not min_limit <= x_border <= max_limit:
                continue
            if x0 <= x_border <= x1:
                for j, y_border in enumerate(y_borders):
                    if j == len(y_borders) - 1:
                        continue
                    if y0 <= y_border <= y1:
                        for k, z_border in enumerate(z_borders):
                            if k == len(z_borders) - 1:
                                continue
                            if z0 <= z_border <= z1:
                                statuses[i][j][k] = status

    result = 0

    for i, x_border in enumerate(x_borders):
        if i == len(x_borders) - 1:
            continue
        if not min_limit <= x_border <= max_limit:
            continue
        for j, y_border in enumerate(y_borders):
            if j == len(y_borders) - 1:
                continue
            if not min_limit <= y_border <= max_limit:
                continue
            for k, z_border in enumerate(z_borders):
                if k == len(z_borders) - 1:
                    continue
                if not min_limit <= z_border <= max_limit:
                    continue
                result += (
                    statuses[i][j][k] *
                    (x_borders[i + 1] - x_border) *
                    (y_borders[j + 1] - y_border) *
                    (z_borders[k + 1] - z_border)
                )

    return result


class TestClass():

    def test_1(self):
        data = [
            'on x=10..12,y=10..12,z=10..12',
            'on x=11..13,y=11..13,z=11..13',
            'off x=9..11,y=9..11,z=9..11',
            'on x=10..10,y=10..10,z=10..10',
        ]
        assert cube_status(data) == 39

    def test_2(self):
        data = [
            'on x=-20..26,y=-36..17,z=-47..7',
            'on x=-20..33,y=-21..23,z=-26..28',
            'on x=-22..28,y=-29..23,z=-38..16',
            'on x=-46..7,y=-6..46,z=-50..-1',
            'on x=-49..1,y=-3..46,z=-24..28',
            'on x=2..47,y=-22..22,z=-23..27',
            'on x=-27..23,y=-28..26,z=-21..29',
            'on x=-39..5,y=-6..47,z=-3..44',
            'on x=-30..21,y=-8..43,z=-13..34',
            'on x=-22..26,y=-27..20,z=-29..19',
            'off x=-48..-32,y=26..41,z=-47..-37',
            'on x=-12..35,y=6..50,z=-50..-2',
            'off x=-48..-32,y=-32..-16,z=-15..-5',
            'on x=-18..26,y=-33..15,z=-7..46',
            'off x=-40..-22,y=-38..-28,z=23..41',
            'on x=-16..35,y=-41..10,z=-47..6',
            'off x=-32..-23,y=11..30,z=-14..3',
            'on x=-49..-5,y=-3..45,z=-29..18',
            'off x=18..30,y=-20..-8,z=-3..13',
            'on x=-41..9,y=-7..43,z=-33..15',
            'on x=-54112..-39298,y=-85059..-49293,z=-27449..7877',
            'on x=967..23432,y=45373..81175,z=27513..53682',
        ]
        assert cube_status(data) == 590784


def main():
    data = [x.strip() for x in sys.stdin]
    result = cube_status(data)
    print(result)


if __name__ == '__main__':
    main()

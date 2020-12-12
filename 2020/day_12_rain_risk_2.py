#!/usr/bin/env python3

import sys


def ship_distance(data):

    curr_pos = (0, 0)
    waypoint = (-1, 10)

    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }

    for line in data:
        direction = line[0]
        step = int(line[1:])

        if direction in directions:
            waypoint = (
                waypoint[0] + step * directions[direction][0],
                waypoint[1] + step * directions[direction][1]
            )
        elif direction == 'F':
            curr_pos = (
                curr_pos[0] + step * waypoint[0],
                curr_pos[1] + step * waypoint[1]
            )
        else:
            turn = (step // 90) % 4

            if direction == 'L':
                if turn == 1:
                    waypoint = (-waypoint[1], waypoint[0])
                elif turn == 2:
                    waypoint = (-waypoint[0], -waypoint[1])
                elif turn == 3:
                    waypoint = (waypoint[1], -waypoint[0])
            else:
                if turn == 1:
                    waypoint = (waypoint[1], -waypoint[0])
                elif turn == 2:
                    waypoint = (-waypoint[0], -waypoint[1])
                elif turn == 3:
                    waypoint = (-waypoint[1], waypoint[0])

    return abs(curr_pos[0]) + abs(curr_pos[1])


class TestClass():

    def test_stabile_seats(self):
        data = [
            'F10',
            'N3',
            'F7',
            'R90',
            'F11'
        ]

        assert ship_distance(data) == 286


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = ship_distance(data)
    print(result)


if __name__ == '__main__':
    main()

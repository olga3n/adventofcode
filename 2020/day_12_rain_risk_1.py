#!/usr/bin/env python3

import sys


def ship_distance(data):

    curr_pos = (0, 0)
    curr_direction = 'E'

    directions = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }

    turns = {
        'N': {'L': ['N', 'W', 'S', 'E'], 'R': ['N', 'E', 'S', 'W']},
        'S': {'L': ['S', 'E', 'N', 'W'], 'R': ['S', 'W', 'N', 'E']},
        'E': {'L': ['E', 'N', 'W', 'S'], 'R': ['E', 'S', 'W', 'N']},
        'W': {'L': ['W', 'S', 'E', 'N'], 'R': ['W', 'N', 'E', 'S']}
    }

    for line in data:
        direction = line[0]
        step = int(line[1:])

        if direction in directions:
            curr_pos = (
                curr_pos[0] + step * directions[direction][0],
                curr_pos[1] + step * directions[direction][1]
            )
        elif direction == 'F':
            curr_pos = (
                curr_pos[0] + step * directions[curr_direction][0],
                curr_pos[1] + step * directions[curr_direction][1]
            )
        else:
            curr_direction = turns[curr_direction][direction][(step // 90) % 4]

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

        assert ship_distance(data) == 25


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = ship_distance(data)
    print(result)


if __name__ == '__main__':
    main()

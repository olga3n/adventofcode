#!/usr/bin/env python3

import sys


def trajectory_trees(data, tree='#', step=(1, 3)):
    result = 0

    i, j = 0, 0

    while i != len(data) - 1:
        i += step[0]
        j += step[1]

        if j >= len(data[0]):
            j -= len(data[0])

        if data[i][j] == tree:
            result += 1

    return result


class TestClass:

    def test_1(self):
        data = [
            '..##.......',
            '#...#...#..',
            '.#....#..#.',
            '..#.#...#.#',
            '.#...##..#.',
            '..#.##.....',
            '.#.#.#....#',
            '.#........#',
            '#.##...#...',
            '#...##....#',
            '.#..#...#.#'
        ]

        assert trajectory_trees(data) == 7


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = trajectory_trees(data)
    print(result)


if __name__ == '__main__':
    main()

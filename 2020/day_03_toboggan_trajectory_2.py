#!/usr/bin/env python3

import sys


def trajectories_trees_product(data, tree='#'):

    slopes = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
    ]

    i = 0
    slope_column = [0] * len(slopes)
    results = [0] * len(slopes)

    while i != len(data) - 1:
        i += 1

        for ind in range(len(slopes)):
            if i % slopes[ind][0] == 0:
                slope_column[ind] += slopes[ind][1]

                if slope_column[ind] >= len(data[0]):
                    slope_column[ind] -= len(data[0])

                if data[i][slope_column[ind]] == tree:
                    results[ind] += 1

    result = 1

    for item in results:
        result *= item

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

        assert trajectories_trees_product(data) == 336


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = trajectories_trees_product(data)
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
import numpy as np


def direct_line_of_sight(asteroids_map, a, b):

    is_visible = True

    delta = (abs(b[0] - a[0]), abs(b[1] - a[1]))

    for coeff in range(1, max(delta[0], delta[1]) + 1):
        if delta[0] % coeff == 0 and \
                delta[1] % coeff == 0 and \
                (delta[0] // coeff != delta[0] or
                    delta[1] // coeff != delta[1]):

            for step in range(1, coeff + 1):
                if b[0] < a[0]:
                    ii = b[0] + step * (delta[0] // coeff)
                else:
                    ii = b[0] - step * (delta[0] // coeff)

                if b[1] < a[1]:
                    jj = b[1] + step * (delta[1] // coeff)
                else:
                    jj = b[1] - step * (delta[1] // coeff)

                if 0 <= jj < len(asteroids_map) and \
                        0 <= ii < len(asteroids_map[jj]) and \
                        (ii, jj) != b and (ii, jj) != a and \
                        asteroids_map[jj][ii] == '#':

                    is_visible = False

                    break

    return is_visible


def vaporize_asteroids(asteroids_map, list_of_asteroids):
    for pos in list_of_asteroids:
        asteroids_map[pos[0]][pos[1]] = '.'


def get_asteroid_by_index(asteroids_map, station, index):
    prev_rounds_count = 0
    result = None
    index -= 1

    while True:

        list_of_visible = []

        for j in range(len(asteroids_map)):
            for i in range(len(asteroids_map[j])):

                if (i, j) != station and asteroids_map[j][i] == '#':

                    if direct_line_of_sight(asteroids_map, station, (i, j)):

                        x0 = i - station[0]
                        y0 = j - station[1]

                        angle = np.degrees(np.arctan2(y0, x0))

                        if angle < -90:
                            angle += 360

                        list_of_visible.append((angle, (i, j)))

        vaporize_asteroids(asteroids_map, [x[1] for x in list_of_visible])

        if prev_rounds_count + len(list_of_visible) > index:
            rel_index = index - prev_rounds_count
            result = sorted(list_of_visible, key=lambda x: x[0])[rel_index][1]
            break

        prev_rounds_count += len(list_of_visible)

    return result


def count_of_visible_from_pos(asteroids_map, pos):
    count_of_visible = 0

    for j in range(len(asteroids_map)):
        for i in range(len(asteroids_map[j])):

            if (i, j) != pos and asteroids_map[j][i] == '#':

                if direct_line_of_sight(asteroids_map, pos, (i, j)):
                    count_of_visible += 1

    return count_of_visible


def best_location(asteroids_map):

    best_score = -1
    best_pos = (0, 0)

    for j in range(len(asteroids_map)):
        for i in range(len(asteroids_map[j])):
            if asteroids_map[j][i] == '#':
                score = count_of_visible_from_pos(asteroids_map, (i, j))

                if score > best_score:
                    best_score = score
                    best_pos = (i, j)

    return (best_pos, best_score)


def parse_input(data):
    return [list(x.strip()) for x in data if len(x.strip())]


def main():
    data = sys.stdin.readlines()
    asteroids_map = parse_input(data)

    pos_station, score = best_location(asteroids_map)

    pos_200 = get_asteroid_by_index(asteroids_map, pos_station, 200)

    print(pos_200[0] * 100 + pos_200[1])


class TestClass:
    def test_get_asteroid_by_index_0(self):
        data = [
            '.#..##.###...#######',
            '##.############..##.',
            '.#.######.########.#',
            '.###.#######.####.#.',
            '#####.##.#.##.###.##',
            '..#####..#.#########',
            '####################',
            '#.####....###.#.#.##',
            '##.#################',
            '#####.##.###..####..',
            '..######..##.#######',
            '####.##.####...##..#',
            '.#####..#.######.###',
            '##...#.##########...',
            '#.##########.#######',
            '.####.#.###.###.#.##',
            '....##.##.###..#####',
            '.#.#.###########.###',
            '#.#.#.#####.####.###',
            '###.##.####.##.#..##'
        ]

        asteroids_map = parse_input(data)
        station, score = best_location(asteroids_map)

        pos_200 = get_asteroid_by_index(asteroids_map, station, 200)

        assert pos_200 == (8, 2)


if __name__ == '__main__':
    main()

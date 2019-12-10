#!/usr/bin/env python3

import sys


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
    return [x.strip() for x in data if len(x.strip())]


def main():
    data = sys.stdin.readlines()
    asteroids_map = parse_input(data)

    pos, score = best_location(asteroids_map)

    print(score)


class TestClass:
    def test_best_location_score_0(self):
        data = [
            '.#..#',
            '.....',
            '#####',
            '....#',
            '...##'
        ]

        asteroids_map = parse_input(data)
        pos, score = best_location(asteroids_map)

        assert (pos == (3, 4)) and (score == 8)

    def test_best_location_score_1(self):
        data = [
            '......#.#.',
            '#..#.#....',
            '..#######.',
            '.#.#.###..',
            '.#..#.....',
            '..#....#.#',
            '#..#....#.',
            '.##.#..###',
            '##...#..#.',
            '.#....####'
        ]

        asteroids_map = parse_input(data)
        pos, score = best_location(asteroids_map)

        assert (pos == (5, 8)) and (score == 33)

    def test_best_location_score_2(self):
        data = [
            '#.#...#.#.',
            '.###....#.',
            '.#....#...',
            '##.#.#.#.#',
            '....#.#.#.',
            '.##..###.#',
            '..#...##..',
            '..##....##',
            '......#...',
            '.####.###.'
        ]

        asteroids_map = parse_input(data)
        pos, score = best_location(asteroids_map)

        assert (pos == (1, 2)) and (score == 35)

    def test_best_location_score_3(self):
        data = [
            '.#..#..###',
            '####.###.#',
            '....###.#.',
            '..###.##.#',
            '##.##.#.#.',
            '....###..#',
            '..#.#..#.#',
            '#..#.#.###',
            '.##...##.#',
            '.....#.#..'
        ]

        asteroids_map = parse_input(data)
        pos, score = best_location(asteroids_map)

        assert (pos == (6, 3)) and (score == 41)

    def test_best_location_score_4(self):
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
        pos, score = best_location(asteroids_map)

        assert (pos == (11, 13)) and (score == 210)


if __name__ == '__main__':
    main()

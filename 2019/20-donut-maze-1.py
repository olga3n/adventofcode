#!/usr/bin/env python3

import sys
from collections import deque


def path_len(maze, portals_int, portals_ext, start, finish):
    p_ext_pos = {v: k for k, v in portals_ext.items()}
    p_int_pos = {v: k for k, v in portals_int.items()}

    start_pos = portals_ext[start]
    end_pos = portals_ext[finish]

    used = set()

    depth = 0

    q = deque([(start_pos, depth)])

    while len(q):
        pos, depth = q.popleft()

        if pos == end_pos:
            break

        if pos in used:
            continue

        used.add(pos)

        ii, jj = pos

        if pos in p_ext_pos and p_ext_pos[pos] in portals_int:
            q.append((portals_int[p_ext_pos[pos]], depth + 1))

        if pos in p_int_pos and p_int_pos[pos] in portals_ext:
            q.append((portals_ext[p_int_pos[pos]], depth + 1))

        if maze[ii - 1][jj] == '.' and (ii - 1, jj) not in used:
            q.append(((ii - 1, jj), depth + 1))
        if maze[ii + 1][jj] == '.' and (ii + 1, jj) not in used:
            q.append(((ii + 1, jj), depth + 1))
        if maze[ii][jj - 1] == '.' and (ii, jj - 1) not in used:
            q.append(((ii, jj - 1), depth + 1))
        if maze[ii][jj + 1] == '.' and (ii, jj + 1) not in used:
            q.append(((ii, jj + 1), depth + 1))

    return depth


def parse_input(data):
    min_sharp_i = len(data) - 1
    max_sharp_i = 0

    min_sharp_j = len(data[0]) - 1
    max_sharp_j = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '#':
                min_sharp_i = min(min_sharp_i, i)
                max_sharp_i = max(max_sharp_i, i)

                min_sharp_j = min(min_sharp_j, j)
                max_sharp_j = max(max_sharp_j, j)

    portals_int = {}
    portals_ext = {}

    for i in range(len(data)):
        for j in range(len(data[i])):
            if 'A' <= data[i][j] <= 'Z':
                if i < len(data) - 2 and \
                        'A' <= data[i + 1][j] <= 'Z' and \
                        data[i + 2][j] == '.':
                    key = data[i][j] + data[i + 1][j]
                    value = (i + 2, j)

                    if i + 2 == min_sharp_i:
                        portals_ext[key] = value
                    else:
                        portals_int[key] = value
                elif i > 1 and \
                        'A' <= data[i - 1][j] <= 'Z' and \
                        data[i - 2][j] == '.':
                    key = data[i - 1][j] + data[i][j]
                    value = (i - 2, j)

                    if i - 2 == max_sharp_i:
                        portals_ext[key] = value
                    else:
                        portals_int[key] = value
                elif j < len(data[i]) - 2 and \
                        'A' <= data[i][j + 1] <= 'Z' and \
                        data[i][j + 2] == '.':
                    key = data[i][j] + data[i][j + 1]
                    value = (i, j + 2)

                    if j + 2 == min_sharp_j:
                        portals_ext[key] = value
                    else:
                        portals_int[key] = value
                elif j > 1 and \
                        'A' <= data[i][j - 1] <= 'Z' and \
                        data[i][j - 2] == '.':
                    key = data[i][j - 1] + data[i][j]
                    value = (i, j - 2)

                    if j - 2 == max_sharp_j:
                        portals_ext[key] = value
                    else:
                        portals_int[key] = value

    return data, portals_int, portals_ext


class TestClass:
    def test_path_len_0(self):
        data = [
            '         A         ',
            '         A         ',
            '  #######.#########',
            '  #######.........#',
            '  #######.#######.#',
            '  #######.#######.#',
            '  #######.#######.#',
            '  #####  B    ###.#',
            'BC...##  C    ###.#',
            '  ##.##       ###.#',
            '  ##...DE  F  ###.#',
            '  #####    G  ###.#',
            '  #########.#####.#',
            'DE..#######...###.#',
            '  #.#########.###.#',
            'FG..#########.....#',
            '  ###########.#####',
            '             Z     ',
            '             Z     ']

        maze, portals_int, portals_ext = parse_input(data)
        result = path_len(maze, portals_int, portals_ext, 'AA', 'ZZ')

        assert result == 23

    def test_path_len_1(self):
        data = [
            '                   A               ',
            '                   A               ',
            '  #################.#############  ',
            '  #.#...#...................#.#.#  ',
            '  #.#.#.###.###.###.#########.#.#  ',
            '  #.#.#.......#...#.....#.#.#...#  ',
            '  #.#########.###.#####.#.#.###.#  ',
            '  #.............#.#.....#.......#  ',
            '  ###.###########.###.#####.#.#.#  ',
            '  #.....#        A   C    #.#.#.#  ',
            '  #######        S   P    #####.#  ',
            '  #.#...#                 #......VT',
            '  #.#.#.#                 #.#####  ',
            '  #...#.#               YN....#.#  ',
            '  #.###.#                 #####.#  ',
            'DI....#.#                 #.....#  ',
            '  #####.#                 #.###.#  ',
            'ZZ......#               QG....#..AS',
            '  ###.###                 #######  ',
            'JO..#.#.#                 #.....#  ',
            '  #.#.#.#                 ###.#.#  ',
            '  #...#..DI             BU....#..LF',
            '  #####.#                 #.#####  ',
            'YN......#               VT..#....QG',
            '  #.###.#                 #.###.#  ',
            '  #.#...#                 #.....#  ',
            '  ###.###    J L     J    #.#.###  ',
            '  #.....#    O F     P    #.#...#  ',
            '  #.###.#####.#.#####.#####.###.#  ',
            '  #...#.#.#...#.....#.....#.#...#  ',
            '  #.#####.###.###.#.#.#########.#  ',
            '  #...#.#.....#...#.#.#.#.....#.#  ',
            '  #.###.#####.###.###.#.#.#######  ',
            '  #.#.........#...#.............#  ',
            '  #########.###.###.#############  ',
            '           B   J   C               ',
            '           U   P   P               ']

        maze, portals_int, portals_ext = parse_input(data)
        result = path_len(maze, portals_int, portals_ext, 'AA', 'ZZ')

        assert result == 58


if __name__ == '__main__':
    data = sys.stdin.readlines()

    maze, portals_int, portals_ext = parse_input(data)

    result = path_len(maze, portals_int, portals_ext, 'AA', 'ZZ')

    print(result)

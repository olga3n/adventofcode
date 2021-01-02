#!/usr/bin/env python3

import sys


def black_tiles(data, days=100):
    tiles = {(0, 0): 0}

    shifts = {
        'e': (0, -2),
        'se': (2, -1),
        'sw': (2, 1),
        'w': (0, 2),
        'nw': (-2, 1),
        'ne': (-2, -1)
    }

    for line in data:
        curr_pos = (0, 0)
        curr_direction = ''

        for i, char in enumerate(line):
            if char in {'s', 'n'}:
                curr_direction = char
            else:
                curr_direction += char

                shift = shifts[curr_direction]

                curr_pos = (
                    curr_pos[0] + shift[0],
                    curr_pos[1] + shift[1]
                )

                if curr_pos not in tiles:
                    tiles[curr_pos] = 0

                if i == len(line) - 1:
                    tiles[curr_pos] = (tiles[curr_pos] + 1) % 2

                curr_direction = ''

    for i in range(days):
        new_tiles = {}

        for pos, color in tiles.items():
            new_tiles[pos] = color

            if color == 1:
                for shift in shifts.values():
                    curr_pos = (
                        pos[0] + shift[0],
                        pos[1] + shift[1]
                    )

                    if curr_pos not in tiles:
                        new_tiles[curr_pos] = 0

        tiles = new_tiles

        new_tiles = {}

        for pos, color in tiles.items():
            black_score = 0

            for shift in shifts.values():
                curr_pos = (
                    pos[0] + shift[0],
                    pos[1] + shift[1]
                )

                if curr_pos in tiles and tiles[curr_pos] == 1:
                    black_score += 1

            if color == 1 and (black_score == 0 or black_score > 2):
                color = 0

            if color == 0 and black_score == 2:
                color = 1

            new_tiles[pos] = color

        tiles = new_tiles

    return sum(tiles.values())


class TestClass():

    def test_black_tiles(self):
        data = [
            'sesenwnenenewseeswwswswwnenewsewsw',
            'neeenesenwnwwswnenewnwwsewnenwseswesw',
            'seswneswswsenwwnwse',
            'nwnwneseeswswnenewneswwnewseswneseene',
            'swweswneswnenwsewnwneneseenw',
            'eesenwseswswnenwswnwnwsewwnwsene',
            'sewnenenenesenwsewnenwwwse',
            'wenwwweseeeweswwwnwwe',
            'wsweesenenewnwwnwsenewsenwwsesesenwne',
            'neeswseenwwswnwswswnw',
            'nenwswwsewswnenenewsenwsenwnesesenew',
            'enewnwewneswsewnwswenweswnenwsenwsw',
            'sweneswneswneneenwnewenewwneswswnese',
            'swwesenesewenwneswnwwneseswwne',
            'enesenwswwswneneswsenwnewswseenwsese',
            'wnwnesenesenenwwnenwsewesewsesesew',
            'nenewswnwewswnenesenwnesewesw',
            'eneswnwswnwsenenwnwnwwseeswneewsenese',
            'neswnwewnwnwseenwseesewsenwsweewe',
            'wseweeenwnesenwwwswnew'
        ]

        assert black_tiles(data) == 2208


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = black_tiles(data)
    print(result)


if __name__ == '__main__':
    main()

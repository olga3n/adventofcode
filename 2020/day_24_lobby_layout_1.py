#!/usr/bin/env python3

import sys


def black_tiles(data):
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

        assert black_tiles(data) == 10


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = black_tiles(data)
    print(result)


if __name__ == '__main__':
    main()

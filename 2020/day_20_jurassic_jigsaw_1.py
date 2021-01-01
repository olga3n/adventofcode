#!/usr/bin/env python3

import sys


class Tile:

    def __init__(self, tile_id, tile_data):
        self.tile_id = tile_id
        self.borders = self.calc_borders(tile_data)

    def calc_borders(self, tile_data):
        return {
            'top': tile_data[0],
            'bottom': tile_data[-1],
            'left': ''.join([x[0] for x in tile_data]),
            'right': ''.join([x[-1] for x in tile_data])
        }


def parse_tiles(data):
    tiles = []

    tile_id = None
    current_tile_data = []

    for line in data:
        if not len(line):
            continue

        if line.startswith('Tile'):
            if tile_id:
                new_tile = Tile(tile_id, current_tile_data)
                tiles.append(new_tile)

            tile_id = int(line.split(' ')[1][:-1])
            current_tile_data = []
        else:
            current_tile_data.append(line)

    if len(current_tile_data):
        new_tile = Tile(tile_id, current_tile_data)
        tiles.append(new_tile)

    return tiles


def corners_score(data):
    tiles = parse_tiles(data)

    stat = {}

    for tile in tiles:
        for _, v in tile.borders.items():
            if v not in stat:
                stat[v] = [tile.tile_id]
                stat[v[::-1]] = [tile.tile_id]
            else:
                stat[v].append(tile.tile_id)
                stat[v[::-1]] = [tile.tile_id]

    matched_tiles = {}

    for k, v in stat.items():
        if len(v) != 1:
            for tile_id in v:
                if tile_id not in matched_tiles:
                    matched_tiles[tile_id] = []

                matched_tiles[tile_id] += [x for x in v if x != tile_id]

    result = 1

    for k, v in matched_tiles.items():
        if len(v) == 2:
            result *= k

    return result


class TestClass():

    def test_corners_score(self):

        data = [
            'Tile 2311:',
            '..##.#..#.',
            '##..#.....',
            '#...##..#.',
            '####.#...#',
            '##.##.###.',
            '##...#.###',
            '.#.#.#..##',
            '..#....#..',
            '###...#.#.',
            '..###..###',
            '',
            'Tile 1951:',
            '#.##...##.',
            '#.####...#',
            '.....#..##',
            '#...######',
            '.##.#....#',
            '.###.#####',
            '###.##.##.',
            '.###....#.',
            '..#.#..#.#',
            '#...##.#..',
            '',
            'Tile 1171:',
            '####...##.',
            '#..##.#..#',
            '##.#..#.#.',
            '.###.####.',
            '..###.####',
            '.##....##.',
            '.#...####.',
            '#.##.####.',
            '####..#...',
            '.....##...',
            '',
            'Tile 1427:',
            '###.##.#..',
            '.#..#.##..',
            '.#.##.#..#',
            '#.#.#.##.#',
            '....#...##',
            '...##..##.',
            '...#.#####',
            '.#.####.#.',
            '..#..###.#',
            '..##.#..#.',
            '',
            'Tile 1489:',
            '##.#.#....',
            '..##...#..',
            '.##..##...',
            '..#...#...',
            '#####...#.',
            '#..#.#.#.#',
            '...#.#.#..',
            '##.#...##.',
            '..##.##.##',
            '###.##.#..',
            '',
            'Tile 2473:',
            '#....####.',
            '#..#.##...',
            '#.##..#...',
            '######.#.#',
            '.#...#.#.#',
            '.#########',
            '.###.#..#.',
            '########.#',
            '##...##.#.',
            '..###.#.#.',
            '',
            'Tile 2971:',
            '..#.#....#',
            '#...###...',
            '#.#.###...',
            '##.##..#..',
            '.#####..##',
            '.#..####.#',
            '#..#.#..#.',
            '..####.###',
            '..#.#.###.',
            '...#.#.#.#',
            '',
            'Tile 2729:',
            '...#.#.#.#',
            '####.#....',
            '..#.#.....',
            '....#..#.#',
            '.##..##.#.',
            '.#.####...',
            '####.#.#..',
            '##.####...',
            '##..#.##..',
            '#.##...##.',
            '',
            'Tile 3079:',
            '#.#.#####.',
            '.#..######',
            '..#.......',
            '######....',
            '####.#..#.',
            '.#...#.##.',
            '#.#####.##',
            '..#.###...',
            '..#.......',
            '..#.###...'
        ]

        assert corners_score(data) == 20899048083289


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = corners_score(data)
    print(result)


if __name__ == '__main__':
    main()

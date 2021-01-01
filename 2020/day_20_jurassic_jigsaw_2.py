#!/usr/bin/env python3

import sys


class Tile:

    def __init__(self, tile_id, tile_data):
        self.tile_id = tile_id
        self.tile_data = tile_data
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


def turn_tile(tile, turn):

    if turn['top'] == 'bottom' or turn['bottom'] == 'top':
        tile.tile_data = tile.tile_data[::-1]

    if turn['left'] == 'right' or turn['right'] == 'left':
        tile.tile_data = [x[::-1] for x in tile.tile_data]

    if turn['top'] == 'left' or turn['bottom'] == 'right':
        tile.tile_data = [
            ''.join(tile.tile_data[j][i] for j in range(len(tile.tile_data)))
            for i in range(len(tile.tile_data[0]))
        ]

        if turn['left'] == 'bottom' or turn['right'] == 'top':
            tile.tile_data = [x[::-1] for x in tile.tile_data]

    if turn['top'] == 'right' or turn['bottom'] == 'left':
        tile.tile_data = [
            ''.join(tile.tile_data[j][i] for j in range(len(tile.tile_data)))
            for i in range(len(tile.tile_data[0]))
        ]

        tile.tile_data = tile.tile_data[::-1]

        if turn['left'] == 'bottom' or turn['right'] == 'top':
            tile.tile_data = [x[::-1] for x in tile.tile_data]

    return tile


def build_image(tiles):
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

    corners = []

    for k, v in matched_tiles.items():
        if len(v) == 2:
            corners.append(k)

    board = []
    square_size = int(pow(len(tiles), 1 / 2))

    for i in range(square_size):
        board.append([None] * square_size)

    board[0][0] = corners[0]
    board[0][1] = matched_tiles[corners[0]][0]
    board[1][0] = matched_tiles[corners[0]][1]
    board[1][1] = (
        set(matched_tiles[board[0][1]])
        .intersection(set(matched_tiles[board[1][0]]))
        .difference({board[0][0]})
        .pop()
    )

    used = {board[0][0], board[0][1], board[1][0], board[1][1]}

    for d in range(2, square_size):

        for i in range(d - 2, -1, -1):
            board[i][d] = [
                x for x in matched_tiles[board[i][d - 1]]
                if x not in used][0]

            board[d][i] = [
                x for x in matched_tiles[board[d - 1][i]]
                if x not in used][0]

            used.add(board[i][d])
            used.add(board[d][i])

        for ii, jj in [(d - 1, d), (d, d - 1), (d, d)]:
            board[ii][jj] = (
                set(matched_tiles[board[ii - 1][jj]])
                .intersection(set(matched_tiles[board[ii][jj - 1]]))
                .difference({board[ii - 1][jj - 1]})
                .pop()
            )

            used.add(board[ii][jj])

    tiles_dict = {}

    for tile in tiles:
        tiles_dict[tile.tile_id] = tile

    directions = [
        (-1, 0, "top"),
        (0, 1, "right"),
        (1, 0, "bottom"),
        (0, -1, "left")
    ]

    for i in range(len(board)):
        for j in range(len(board[i])):

            curr_tile = tiles_dict[board[i][j]]
            curr_turn = {}

            for ii, jj, name in directions:
                if (ii != 0 and jj != 0) or ii == jj:
                    continue

                if (0 <= i + ii < len(board) and
                        0 <= j + jj < len(board[i])):
                    next_tile = tiles_dict[board[i + ii][j + jj]]

                    for direction, border in curr_tile.borders.items():
                        if border in next_tile.borders.values():
                            curr_turn[name] = direction
                            break

                        if border[::-1] in next_tile.borders.values():
                            curr_turn[name] = direction
                            break

                if name not in curr_turn:
                    curr_turn[name] = None

            tiles_dict[board[i][j]] = turn_tile(curr_tile, curr_turn)

    img = []
    size = len(tiles_dict[board[0][0]].tile_data)

    for i in range(len(board)):
        for k in range(1, size - 1):
            new_line = ''

            for j in range(len(board[i])):
                new_line += tiles_dict[board[i][j]].tile_data[k][1:-1]

            img.append(new_line)

    return img


def count_monsters(img, monster):
    count = 0

    for i in range(len(img) - len(monster) + 1):
        for j in range(len(img[i]) - len(monster[0]) + 1):
            is_monster = True

            for ii in range(len(monster)):
                for jj in range(len(monster[ii])):
                    if monster[ii][jj] == '#' and img[i + ii][j + jj] != '#':
                        is_monster = False
                        break

                if not is_monster:
                    break

            if is_monster:
                count += 1

    return count


def calc_cells(img):
    result = 0

    for line in img:
        result += len([1 for x in line if x == '#'])

    return result


def sea_monster_score(data):
    tiles = parse_tiles(data)
    img = build_image(tiles)

    monster = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ]

    monsters = count_monsters(img, monster)

    directions = ['left', 'right', 'top', 'bottom']
    img_cells = calc_cells(img)
    monster_cells = calc_cells(monster)

    for d1 in directions:
        for d2 in directions:
            new_turn = {'left': d1, 'top': d2, 'right': None, 'bottom': None}
            new_img = turn_tile(Tile(0, img), new_turn).tile_data

            monsters = count_monsters(new_img, monster)

            if monsters > 0:
                return img_cells - monsters * monster_cells


class TestClass():

    def test_sea_monster_score(self):

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

        assert sea_monster_score(data) == 273


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = sea_monster_score(data)
    print(result)


if __name__ == '__main__':
    main()

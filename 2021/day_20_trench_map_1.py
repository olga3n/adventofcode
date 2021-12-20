#!/usr/bin/env python3

import sys
from typing import List


def expand_image(image: List[List[str]], symbol: str) -> List[List[str]]:
    image = [[symbol] * 3 + row + [symbol] * 3 for row in image]
    empty_row = [symbol] * len(image[0])
    image = (
        [empty_row.copy(), empty_row.copy(), empty_row.copy()] +
        image +
        [empty_row.copy(), empty_row.copy(), empty_row.copy()]
    )
    return image


def process_image(
    image: List[List[str]], info: str, step: int
) -> List[List[str]]:

    if info[0] == '#' and step % 2 == 1:
        image = expand_image(image, '#')
    else:
        image = expand_image(image, '.')

    new_img = []

    for i in range(len(image)):
        new_img.append(image[i].copy())
        for j in range(len(image[i])):
            bit_str = ''
            for ii in [-1, 0, 1]:
                for jj in [-1, 0, 1]:
                    if not 0 <= i + ii < len(image):
                        continue
                    if not 0 <= j + jj < len(image[i]):
                        continue
                    bit_str += '1' if image[i + ii][j + jj] == '#' else '0'

            if len(bit_str) != 9:
                bit_str = ('1' if image[i][j] == '#' else '0') * 9

            new_img[i][j] = info[int(bit_str, 2)]

    return new_img


def image_pixels(data: List[str], steps: int = 2) -> int:
    info = data[0]
    image = [list(data[i]) for i in range(2, len(data))]

    for step in range(steps):
        image = process_image(image, info, step)

    return sum([row.count('#') for row in image])


class TestClass():

    def test_1(self):
        data = [
            '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##' +
            '#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###' +
            '.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.' +
            '.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....' +
            '.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..' +
            '...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....' +
            '..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#',
            '',
            '#..#.',
            '#....',
            '##..#',
            '..#..',
            '..###',
        ]
        assert image_pixels(data) == 35


def main():
    data = [x.strip() for x in sys.stdin]
    result = image_pixels(data)
    print(result)


if __name__ == '__main__':
    main()

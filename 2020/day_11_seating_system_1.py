#!/usr/bin/env python3

import sys


def calc_occupied_seats(data, i, j):
    occupied_seats = 0

    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:

            if di == 0 and dj == 0:
                continue

            if i + di < 0 or i + di >= len(data):
                continue

            if j + dj < 0 or j + dj >= len(data[i]):
                continue

            if data[i + di][j + dj] == '#':
                occupied_seats += 1

    return occupied_seats


def stabile_seats(data):
    while True:
        new_data = []

        for i in range(len(data)):
            new_line = ''

            for j in range(len(data[i])):

                if data[i][j] == '.':
                    new_line += '.'
                    continue

                occupied_seats = calc_occupied_seats(data, i, j)

                if data[i][j] == 'L' and occupied_seats == 0:
                    new_line += '#'
                elif data[i][j] == '#' and occupied_seats >= 4:
                    new_line += 'L'
                else:
                    new_line += data[i][j]

            new_data.append(new_line)

        if data == new_data:
            break

        data = new_data

    result = 0

    for line in data:
        result += len([x for x in line if x == '#'])

    return result


class TestClass():

    def test_stabile_seats(self):
        data = [
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL'
        ]

        assert stabile_seats(data) == 37


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = stabile_seats(data)
    print(result)


if __name__ == '__main__':
    main()

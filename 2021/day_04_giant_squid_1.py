#!/usr/bin/env python3

import sys
from typing import List


def bingo_status(board: List[List[int]]) -> bool:
    for row in board:
        if sum([1 for x in row if x == 0]) == len(row):
            return True

    for i in range(len(board[0])):
        if sum([1 for x in board if x[i] == 0]) == len(board):
            return True

    return False


def sum_scores(board: List[List[int]]) -> int:
    return sum([sum(row) for row in board])


def bingo_score(data: List[str]) -> int:
    vector = list(map(int, data[0].split(',')))
    boards = []

    new_board = []

    for line in data[2:]:
        if len(line):
            new_board.append(list(map(int, line.split())))
        else:
            boards.append(new_board)
            new_board = []

    boards.append(new_board)

    result = 0

    for value in vector:
        for board in boards:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == value:
                        board[i][j] = 0
            if bingo_status(board):
                result = sum_scores(board) * value
                return result

    return result


class TestClass():

    def test_1(self):
        data = [
            '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
            '',
            '22 13 17 11  0',
            ' 8  2 23  4 24',
            '21  9 14 16  7',
            ' 6 10  3 18  5',
            ' 1 12 20 15 19',
            '',
            ' 3 15  0  2 22',
            ' 9 18 13 17  5',
            '19  8  7 25 23',
            '20 11 10 24  4',
            '14 21 16 12  6',
            '',
            '14 21 17 24  4',
            '10 16 15  9 19',
            '18  8 23 26 20',
            '22 11 13  6  5',
            ' 2  0 12  3  7',
        ]

        assert bingo_score(data) == 4512


def main():
    data = [x.strip() for x in sys.stdin]
    result = bingo_score(data)
    print(result)


if __name__ == '__main__':
    main()

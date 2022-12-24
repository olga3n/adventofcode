#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

WALK_DIFFS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}

TURNS = {
    ('>', 'L'): '^',
    ('>', 'R'): 'v',
    ('<', 'L'): 'v',
    ('<', 'R'): '^',
    ('v', 'L'): '>',
    ('v', 'R'): '<',
    ('^', 'L'): '<',
    ('^', 'R'): '>',
}

DIRECTION_SCORE = {
    '>': 0,
    'v': 1,
    '<': 2,
    '^': 3
}

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


@dataclass
class Face:
    start_row: int
    start_column: int
    square: List[str]
    adj: List[Optional[Tuple['Face', int]]]


def parse_path(raw_path: str) -> List[str]:
    path = []

    curr_number = ''

    for symbol in raw_path:
        if symbol.isdigit():
            curr_number += symbol
        else:
            path.append(curr_number)
            path.append(symbol)
            curr_number = ''

    if curr_number:
        path.append(curr_number)

    return path


def walk(
    face: Face, pos: Tuple[int, int], direction: str, step: int
) -> Tuple[Face, Tuple[int, int], int]:

    diff = WALK_DIFFS[direction]

    for i in range(step):
        row = pos[0] + diff[0]
        column = pos[1] + diff[1]
        new_face = face
        new_direction = direction
        turn = 0

        if row < 0:
            row = len(face.square) - 1
            new_face, turn = face.adj[UP]
            if turn == 1:
                new_direction = '<'
            elif turn == 2:
                new_direction = 'v'
            elif turn == 3:
                new_direction = '>'
        if row == len(face.square):
            row = 0
            new_face, turn = face.adj[DOWN]
            if turn == 1:
                new_direction = '>'
            elif turn == 2:
                new_direction = '^'
            elif turn == 3:
                new_direction = '<'
        if column < 0:
            column = len(face.square) - 1
            new_face, turn = face.adj[LEFT]
            if turn == 1:
                new_direction = 'v'
            elif turn == 2:
                new_direction = '>'
            elif turn == 3:
                new_direction = '^'
        if column == len(face.square):
            column = 0
            new_face, turn = face.adj[RIGHT]
            if turn == 1:
                new_direction = '^'
            elif turn == 2:
                new_direction = '<'
            elif turn == 3:
                new_direction = 'v'

        if turn == 1:
            row, column = len(new_face.square) - column - 1, row
        elif turn == 2:
            row, column = (
                len(new_face.square) - row - 1,
                len(new_face.square) - column - 1
            )
        elif turn == 3:
            row, column = column, len(new_face.square) - row - 1

        if new_face.square[row][column] == '#':
            return face, pos, direction

        if new_face.square[row][column] == '.':
            pos = (row, column)
            face = new_face
            direction = new_direction
            diff = WALK_DIFFS[direction]

    return face, pos, direction


def final_pos_score(data: List[str], face_size: int) -> int:
    field = [line.rstrip() for line in data if len(line.rstrip())]
    field, path = field[:-1], parse_path(field[-1])
    max_row = max(len(line) for line in field)
    field = [line.ljust(max_row, ' ') for line in field]

    faces = {}

    for i in range(0, len(field), face_size):
        for j in range(0, len(field[i]), face_size):
            if field[i][j] == ' ':
                continue
            square = [
                line[j: j + face_size] for line in field[i: i + face_size]
            ]
            faces[(i // face_size, j // face_size)] = Face(
                start_row=i,
                start_column=j,
                square=square,
                adj=[None, None, None, None]
            )

    for (x, y), face in faces.items():
        if (x - 1, y) in faces:
            face.adj[UP] = (faces[(x - 1, y)], 0)
        if (x + 1, y) in faces:
            face.adj[DOWN] = (faces[(x + 1, y)], 0)
        if (x, y - 1) in faces:
            face.adj[LEFT] = (faces[(x, y - 1)], 0)
        if (x, y + 1) in faces:
            face.adj[RIGHT] = (faces[(x, y + 1)], 0)

    CLOCKWISE_PAIRS = (
        (UP, RIGHT),
        (RIGHT, DOWN),
        (DOWN, LEFT),
        (LEFT, UP)
    )

    for _ in range(3):
        for face in faces.values():
            for d1, d2 in CLOCKWISE_PAIRS:
                if face.adj[d1] and face.adj[d2]:
                    face_1, shift_1 = face.adj[d1]
                    face_2, shift_2 = face.adj[d2]
                    face_1_adj = face_1.adj[-shift_1:] + face_1.adj[:-shift_1]
                    face_2_adj = face_2.adj[-shift_2:] + face_2.adj[:-shift_2]
                    if not face_1_adj[d2] and not face_2_adj[d1]:
                        face_1.adj[(d2 - shift_1) % 4] = (
                            face_2, (3 + shift_2 - shift_1) % 4
                        )
                        face_2.adj[(d1 - shift_2) % 4] = (
                            face_1, (1 + shift_1 - shift_2) % 4
                        )

    pos = (0, 0)
    face = min(faces.items())[1]
    direction = '>'

    for item in path:
        if item.isdigit():
            face, pos, direction = walk(
                face, pos, direction, int(item)
            )
        else:
            direction = TURNS[(direction, item)]

    pos = (
        pos[0] + face.start_row,
        pos[1] + face.start_column
    )

    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + DIRECTION_SCORE[direction]


def test_final_pos_score():
    data = [
        '        ...#',
        '        .#..',
        '        #...',
        '        ....',
        '...#.......#',
        '........#...',
        '..#....#....',
        '..........#.',
        '        ...#....',
        '        .....#..',
        '        .#......',
        '        ......#.',
        '',
        '10R5L5R10L4R5L5'
    ]

    assert final_pos_score(data, face_size=4) == 5031


def main():
    data = sys.stdin.readlines()
    result = final_pos_score(data, face_size=50)
    print(result)


if __name__ == '__main__':
    main()

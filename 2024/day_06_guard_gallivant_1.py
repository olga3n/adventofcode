#!/usr/bin/env python3

import sys

TURN_RULES = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^',
}

DIFF_MAP = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}


class GuardMap():

    def __init__(self, lines):
        self.lines = lines

        self.size_r = len(lines)
        self.size_c = len(lines[0])

        self.walk_map = []

        for i in range(self.size_r):
            self.walk_map.append(['.'] * self.size_c)

    def is_valid_pos(self, pos: tuple[int, int]) -> bool:
        if not 0 <= pos[0] < self.size_r:
            return False

        if not 0 <= pos[1] < self.size_c:
            return False

        return True

    def walk(self, guard_direction: str, guard_pos: tuple[int, int]):
        while True:
            self.walk_map[guard_pos[0]][guard_pos[1]] = 'X'

            delta = DIFF_MAP[guard_direction]

            new_guard_pos = (
                guard_pos[0] + delta[0],
                guard_pos[1] + delta[1],
            )

            if not self.is_valid_pos(new_guard_pos):
                break

            if self.lines[new_guard_pos[0]][new_guard_pos[1]] == '#':
                guard_direction = TURN_RULES[guard_direction]
                continue

            guard_pos = new_guard_pos

    def walk_map_pos_cnt(self):
        return sum(
            1
            for line in self.walk_map
            for symbol in line
            if symbol == 'X'
        )


def guard_pos_cnt(lines: list[str]) -> int:
    guard_pos = (0, 0)

    positions = (
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
    )

    for i, j in positions:
        if lines[i][j] == '^':
            guard_pos = (i, j)
            break

    gm = GuardMap(lines)
    gm.walk('^', guard_pos)

    return gm.walk_map_pos_cnt()


def test_guard_pos_cnt():
    lines = [
        '....#.....',
        '.........#',
        '..........',
        '..#.......',
        '.......#..',
        '..........',
        '.#..^.....',
        '........#.',
        '#.........',
        '......#...',
    ]
    assert 41 == guard_pos_cnt(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = guard_pos_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()

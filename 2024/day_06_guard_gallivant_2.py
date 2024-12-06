#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Position():
    x: int
    y: int

    def add(self, other: 'Position'):
        return Position(
            self.x + other.x,
            self.y + other.y,
        )


TURN_RULES = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^',
}

DIFF_MAP = {
    '^': Position(-1, 0),
    '>': Position(0, 1),
    'v': Position(1, 0),
    '<': Position(0, -1),
}


class GuardMap():

    def __init__(self, lines):
        self.lines = lines

        self.size_r = len(lines)
        self.size_c = len(lines[0])

    def is_valid_pos(self, pos: Position) -> bool:
        if not 0 <= pos.x < self.size_r:
            return False

        if not 0 <= pos.y < self.size_c:
            return False

        return True

    def walk(
        self,
        guard_direction: str,
        guard_pos: Position,
        stop_pos: Position = Position(-1, -1),
    ) -> tuple[set[Position], bool]:
        visited: dict[str, set[Position]] = {key: set() for key in DIFF_MAP}
        is_loop = False

        while True:
            if guard_pos in visited[guard_direction]:
                is_loop = True
                break

            visited[guard_direction].add(guard_pos)

            new_guard_pos = guard_pos.add(DIFF_MAP[guard_direction])

            if not self.is_valid_pos(new_guard_pos):
                break

            if (self.lines[new_guard_pos.x][new_guard_pos.y] == '#' or
                    new_guard_pos == stop_pos):
                guard_direction = TURN_RULES[guard_direction]
                continue

            guard_pos = new_guard_pos

        visited_set: set[Position] = set()

        for next_set in visited.values():
            visited_set.update(next_set)

        return visited_set, is_loop


def guard_stop_pos_cnt(lines: list[str]) -> int:
    guard_pos = Position(0, 0)

    positions = (
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
    )

    for i, j in positions:
        if lines[i][j] == '^':
            guard_pos = Position(i, j)
            break

    gm = GuardMap(lines)
    candidates, _ = gm.walk('^', guard_pos)

    result = 0

    for stop_pos in candidates:
        if stop_pos == guard_pos:
            continue

        _, is_loop = gm.walk('^', guard_pos, stop_pos)
        if is_loop:
            result += 1

    return result


def test_guard_stop_pos_cnt():
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
    assert 6 == guard_stop_pos_cnt(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = guard_stop_pos_cnt(lines)
    print(result)


if __name__ == '__main__':
    main()

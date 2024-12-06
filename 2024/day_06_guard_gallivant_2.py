#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Position():
    x: int
    y: int

    def eq_place(self, other) -> bool:
        return self.x == other.x and self.y == other.y


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


@dataclass(frozen=True)
class GuardPosition(Position):
    direction: str

    def next_pos(self) -> 'GuardPosition':
        return GuardPosition(
            self.x + DIFF_MAP[self.direction].x,
            self.y + DIFF_MAP[self.direction].y,
            self.direction,
        )

    def turn(self) -> 'GuardPosition':
        return GuardPosition(
            self.x,
            self.y,
            TURN_RULES[self.direction],
        )


class GuardMap():

    def __init__(self, lines):
        self.lines = lines

        self.size_r = len(lines)
        self.size_c = len(lines[0])

    def is_valid_pos(self, pos: Position) -> bool:
        return (
            0 <= pos.x < self.size_r and
            0 <= pos.y < self.size_c
        )

    def is_wall(self, pos: Position) -> bool:
        return self.lines[pos.x][pos.y] == '#'

    def walk(
        self,
        guard_pos: GuardPosition,
        stop_pos: Position = Position(-1, -1),
    ) -> tuple[dict[Position, GuardPosition], bool]:

        guard_visited: set[GuardPosition] = set()
        pos_visited: dict[Position, GuardPosition] = {}

        while True:
            new_guard_pos = guard_pos.next_pos()

            if not self.is_valid_pos(new_guard_pos):
                break

            if self.is_wall(new_guard_pos) or new_guard_pos.eq_place(stop_pos):
                guard_pos = guard_pos.turn()
                continue

            if new_guard_pos in guard_visited:
                return pos_visited, True

            pos = Position(new_guard_pos.x, new_guard_pos.y)

            if pos not in pos_visited:
                pos_visited[pos] = guard_pos

            guard_visited.add(new_guard_pos)
            guard_pos = new_guard_pos

        return pos_visited, False


def guard_stop_pos_cnt(lines: list[str]) -> int:
    guard_pos = GuardPosition(-1, -1, '^')

    positions = (
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
    )

    for i, j in positions:
        if lines[i][j] == '^':
            guard_pos = GuardPosition(i, j, '^')
            break

    gm = GuardMap(lines)
    candidates, _ = gm.walk(guard_pos)

    result = 0

    for stop_pos, prev_pos in candidates.items():
        if stop_pos.eq_place(guard_pos):
            continue
        _, is_loop = gm.walk(prev_pos, stop_pos)
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

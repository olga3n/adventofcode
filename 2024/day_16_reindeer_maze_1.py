#!/usr/bin/env python3

import sys
from typing import Iterable
from dataclasses import dataclass
import heapq

STEP_DIFF = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
}

TURNS = {
    '>': ('^', 'v'),
    '<': ('^', 'v'),
    'v': ('<', '>'),
    '^': ('<', '>'),
}


@dataclass
class State:
    x: int
    y: int
    score: int
    direction: str

    def __lt__(self, other):
        return self.direction < other.direction


def gen_next(
    lines: list[str], i: int, j: int, direction: str,
) -> Iterable[tuple[int, int, int, str]]:
    xx = i + STEP_DIFF[direction][0]
    yy = j + STEP_DIFF[direction][1]

    flag_1 = (0 <= xx < len(lines))
    flag_2 = (0 <= yy < len(lines[0]))

    if flag_1 and flag_2 and lines[xx][yy] != '#':
        yield xx, yy, 1, direction

    for next_direction in TURNS[direction]:
        yield i, j, 1000, next_direction


def lowest_score(lines: list[str], start='S', end='E') -> int:
    pos = next(iter(
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
        if lines[i][j] == start
    ))

    h: list[State] = []
    heapq.heappush(h, State(pos[0], pos[1], 0, '>'))
    result = -1
    min_score: dict[tuple[int, int, str], int] = {}

    while len(h):
        state = heapq.heappop(h)

        if lines[state.x][state.y] == end:
            if result == -1 or result > state.score:
                result = state.score
            continue

        last_min = min_score.get((state.x, state.y, state.direction), -1)

        if last_min != -1 and last_min < state.score:
            continue

        min_score[(state.x, state.y, state.direction)] = state.score

        next_steps = gen_next(lines, state.x, state.y, state.direction)

        for i, j, score, direction in next_steps:
            if result != -1 and state.score + score > result:
                continue

            last_min = min_score.get((i, j, direction), -1)
            if last_min != -1 and state.score + score > last_min:
                continue

            heapq.heappush(h, State(i, j, state.score + score, direction))

    return result


def test_lowest_score_0():
    lines = [
        '###############',
        '#.......#....E#',
        '#.#.###.#.###.#',
        '#.....#.#...#.#',
        '#.###.#####.#.#',
        '#.#.#.......#.#',
        '#.#.#####.###.#',
        '#...........#.#',
        '###.#.#####.#.#',
        '#...#.....#.#.#',
        '#.#.#.###.#.#.#',
        '#.....#...#.#.#',
        '#.###.#.#.#.#.#',
        '#S..#.....#...#',
        '###############',
    ]
    assert 7036 == lowest_score(lines)


def test_lowest_score_1():
    lines = [
        '#################',
        '#...#...#...#..E#',
        '#.#.#.#.#.#.#.#.#',
        '#.#.#.#...#...#.#',
        '#.#.#.#.###.#.#.#',
        '#...#.#.#.....#.#',
        '#.#.#.#.#.#####.#',
        '#.#...#.#.#.....#',
        '#.#.#####.#.###.#',
        '#.#.#.......#...#',
        '#.#.###.#####.###',
        '#.#.#...#.....#.#',
        '#.#.#.#####.###.#',
        '#.#.#.........#.#',
        '#.#.#.#########.#',
        '#S#.............#',
        '#################',
    ]
    assert 11048 == lowest_score(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = lowest_score(lines)
    print(result)


if __name__ == '__main__':
    main()

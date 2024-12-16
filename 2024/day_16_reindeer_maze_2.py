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
    lines: list[str], i: int, j: int, direction: str, coeff: int = 1,
) -> Iterable[tuple[int, int, int, str]]:
    xx = i + coeff * STEP_DIFF[direction][0]
    yy = j + coeff * STEP_DIFF[direction][1]

    flag_1 = (0 <= xx < len(lines))
    flag_2 = (0 <= yy < len(lines[0]))

    if flag_1 and flag_2 and lines[xx][yy] != '#':
        yield xx, yy, 1, direction

    for next_direction in TURNS[direction]:
        yield i, j, 1000, next_direction


def optimum_tiles(lines: list[str], start='S', end='E') -> int:
    pos = next(iter(
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
        if lines[i][j] == start
    ))

    h: list[State] = []
    heapq.heappush(h, State(pos[0], pos[1], 0, '>'))
    best_score = -1
    min_score: dict[tuple[int, int, str], int] = {}

    while len(h):
        state = heapq.heappop(h)

        last_min = min_score.get((state.x, state.y, state.direction), -1)

        if last_min != -1 and last_min < state.score:
            continue

        min_score[(state.x, state.y, state.direction)] = state.score

        if lines[state.x][state.y] == end:
            if best_score == -1 or best_score > state.score:
                best_score = state.score
            continue

        next_steps = gen_next(lines, state.x, state.y, state.direction)

        for i, j, score, direction in next_steps:
            if best_score != -1 and state.score + score > best_score:
                continue

            last_min = min_score.get((i, j, direction), -1)
            if last_min != -1 and state.score + score > last_min:
                continue

            heapq.heappush(h, State(i, j, state.score + score, direction))

    end_pos = next(iter(
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
        if lines[i][j] == end
    ))

    states = []
    best_tiles = set()

    for (i, j, direction), score in min_score.items():
        if score == best_score and (i, j) == end_pos:
            states.append(State(i, j, score, direction))

    while len(states):
        new_states = []

        for state in states:
            best_tiles.add((state.x, state.y))
            prev_steps = gen_next(lines, state.x, state.y, state.direction, -1)
            for i, j, score, direction in prev_steps:
                prev_score = state.score - score
                if min_score.get((i, j, direction), -1) == prev_score:
                    new_states.append(State(i, j, prev_score, direction))

        states = new_states

    return len(best_tiles)


def test_optimum_tiles_0():
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
    assert 45 == optimum_tiles(lines)


def test_optimum_tiles_1():
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
    assert 64 == optimum_tiles(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = optimum_tiles(lines)
    print(result)


if __name__ == '__main__':
    main()

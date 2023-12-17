#!/usr/bin/env python3

import sys
from typing import List
from dataclasses import dataclass
import heapq

ROTATIONS = {
    '>': ('^', 'v'),
    '<': ('^', 'v'),
    '^': ('<', '>'),
    'v': ('<', '>'),
}

NEXT_DIFF = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0),
}


@dataclass(frozen=True, order=True)
class State:
    x: int
    y: int
    view: str


def min_heat_loss(data: List[List[int]]) -> int:
    end_pos = (
        len(data) - 1,
        len(data[0]) - 1
    )

    result = None
    visited = {}
    states = []

    min_steps, max_steps = 4, 10

    heat = 0

    for i in range(max_steps + 1):
        if i >= len(data[0]):
            break
        if i > 0:
            heat += data[0][i]
        if i >= min_steps:
            heapq.heappush(states, (heat, State(0, i, '>')))

    heat = 0

    for i in range(max_steps + 1):
        if i >= len(data):
            break
        if i > 0:
            heat += data[i][0]
        if i >= min_steps:
            heapq.heappush(states, (heat, State(i, 0, 'v')))

    while states:
        heat, next_state = heapq.heappop(states)

        if next_state in visited and visited[next_state] <= heat:
            continue

        visited[next_state] = heat

        if (next_state.x, next_state.y) == end_pos:
            if not result:
                result = heat
            else:
                result = min(result, heat)

        for rotation in ROTATIONS[next_state.view]:
            dx, dy = NEXT_DIFF[rotation]
            new_heat = heat

            for i in range(1, max_steps + 1):
                xx, yy = next_state.x + i * dx, next_state.y + i * dy
                if not (0 <= xx < len(data) and 0 <= yy < len(data[0])):
                    continue
                new_heat += data[xx][yy]
                if i < min_steps:
                    continue
                new_state = State(xx, yy, rotation)
                if new_state in visited and visited[new_state] <= new_heat:
                    continue
                heapq.heappush(states, (new_heat, new_state))

    return result


def test_min_heat_loss_1():
    data = [
        '2413432311323',
        '3215453535623',
        '3255245654254',
        '3446585845452',
        '4546657867536',
        '1438598798454',
        '4457876987766',
        '3637877979653',
        '4654967986887',
        '4564679986453',
        '1224686865563',
        '2546548887735',
        '4322674655533',
    ]
    data = [list(map(int, line)) for line in data]
    assert min_heat_loss(data) == 94


def test_min_heat_loss_2():
    data = [
        '111111111111',
        '999999999991',
        '999999999991',
        '999999999991',
        '999999999991',
    ]
    data = [list(map(int, line)) for line in data]
    assert min_heat_loss(data) == 71


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [list(map(int, line)) for line in data if len(line)]
    result = min_heat_loss(data)
    print(result)


if __name__ == '__main__':
    main()

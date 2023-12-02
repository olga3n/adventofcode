#!/usr/bin/env python3

import sys
from typing import List
from dataclasses import dataclass


@dataclass
class State:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    game_id: int
    states: List[State]


def parse_games(data):
    for line in data:
        game_prs, states_prs = line.split(': ')
        game_id = int(game_prs.split(' ')[1])
        states = []
        for state_prs in states_prs.split('; '):
            values = {'red': 0, 'green': 0, 'blue': 0}
            for item in state_prs.split(', '):
                value, color = item.split(' ')
                values[color] = int(value)
            states.append(State(**values))
        yield Game(game_id, states)


def min_cubes(game: Game):
    cubes = State(0, 0, 0)
    for state in game.states:
        cubes.red = max(cubes.red, state.red)
        cubes.green = max(cubes.green, state.green)
        cubes.blue = max(cubes.blue, state.blue)
    return cubes


def game_power(game):
    cubes = min_cubes(game)
    return cubes.red * cubes.green * cubes.blue


def sum_powers(data):
    return sum(game_power(game) for game in parse_games(data))


def test_sum_powers():
    data = [
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
    ]
    assert sum_powers(data) == 2286


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = sum_powers(data)
    print(result)


if __name__ == '__main__':
    main()

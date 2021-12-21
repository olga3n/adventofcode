#!/usr/bin/env python3

import sys
from typing import List


def game_score(
        data: List[str], max_score: int = 1000, max_dice: int = 100,
        board_size: int = 10
) -> int:

    positions = [int(x.split(': ')[1]) for x in data]
    scores = [0] * len(positions)
    dice_score = 1
    player_ind = 0
    rolls = 0

    while max(scores) < max_score:
        roll = 0
        for i in range(3):
            roll += dice_score
            dice_score = dice_score % max_dice + 1
            rolls += 1
        positions[player_ind] = (
            (positions[player_ind] + roll - 1) % board_size + 1
        )
        scores[player_ind] += positions[player_ind]
        player_ind = (player_ind + 1) % len(positions)

    return min(scores) * rolls


class TestClass():

    def test_1(self):
        data = [
            'Player 1 starting position: 4',
            'Player 2 starting position: 8'
        ]
        assert game_score(data) == 739785


def main():
    data = [x.strip() for x in sys.stdin]
    result = game_score(data)
    print(result)


if __name__ == '__main__':
    main()

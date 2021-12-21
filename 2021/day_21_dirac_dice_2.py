#!/usr/bin/env python3

import sys
from typing import List, Dict, Tuple


def multiverse_game_score(
        data: List[str], max_score: int = 21, board_size: int = 10
) -> int:

    positions = [int(x.split(': ')[1]) for x in data]

    multiverse_game = {((positions[0], 0), (positions[1], 0)): 1}
    results = [0, 0]
    player_ind = 0

    while len(multiverse_game):
        new_multiverse_game: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}

        for players, cnt in multiverse_game.items():
            pos, score = players[player_ind]

            for i in range(1, 4):
                for j in range(1, 4):
                    for k in range(1, 4):
                        roll = i + j + k
                        new_pos = (pos + roll - 1) % board_size + 1
                        new_score = score + new_pos

                        if new_score >= max_score:
                            results[player_ind] += cnt
                        else:
                            if player_ind == 0:
                                new_game = ((new_pos, new_score), players[1])
                            else:
                                new_game = (players[0], (new_pos, new_score))

                            new_multiverse_game[new_game] = (
                                new_multiverse_game.get(new_game, 0) + cnt
                            )

        multiverse_game = new_multiverse_game
        player_ind = (player_ind + 1) % 2

    return max(results)


class TestClass():

    def test_1(self):
        data = [
            'Player 1 starting position: 4',
            'Player 2 starting position: 8'
        ]
        assert multiverse_game_score(data) == 444356092776315


def main():
    data = [x.strip() for x in sys.stdin]
    result = multiverse_game_score(data)
    print(result)


if __name__ == '__main__':
    main()

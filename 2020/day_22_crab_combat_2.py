#!/usr/bin/env python3

import sys
from collections import deque


def parse_decks(data):
    decks = []
    curr_deck = []

    for line in data:
        if not len(line):
            continue

        if line.startswith('Player'):
            if curr_deck:
                decks.append(curr_deck)
            curr_deck = []
        else:
            curr_deck.append(int(line))

    if curr_deck:
        decks.append(curr_deck)

    return decks


def play_game(decks, subgames_cache):

    cache = set()

    while True:
        record = (tuple(decks[0]), tuple(decks[1]))

        if record in cache:
            winner = 0
            break

        cache.add(record)

        head_1 = decks[0].popleft()
        head_2 = decks[1].popleft()

        if len(decks[0]) >= head_1 and len(decks[1]) >= head_2:
            record = (tuple(decks[0]), tuple(decks[1]))

            if record in subgames_cache:
                winner, score = subgames_cache[record]
            else:
                subgame_deck_1 = deque((list(decks[0])[:head_1]))
                subgame_deck_2 = deque((list(decks[1])[:head_2]))

                winner, score = play_game(
                    [subgame_deck_1, subgame_deck_2], subgames_cache)

                subgames_cache[record] = (winner, score)

            if winner == 0:
                decks[0].append(head_1)
                decks[0].append(head_2)
            else:
                decks[1].append(head_2)
                decks[1].append(head_1)

        elif head_1 > head_2:
            decks[0].append(head_1)
            decks[0].append(head_2)
        else:
            decks[1].append(head_2)
            decks[1].append(head_1)

        if len(decks[1]) == 0:
            winner = 0
            break

        if len(decks[0]) == 0:
            winner = 1
            break

    score = sum([
        (len(decks[winner]) - i) * decks[winner][i]
        for i in range(len(decks[winner]))
    ])

    return winner, score


def winner_score(data):
    decks = parse_decks(data)

    subgames_cache = {}

    winner, score = play_game(
        [deque(decks[0]), deque(decks[1])], subgames_cache)

    return score


class TestClass():

    def test_winner_score_1(self):

        data = [
            'Player 1:',
            '43',
            '19',
            '',
            'Player 2:',
            '2',
            '29',
            '14'
        ]

        assert winner_score(data) == 43 * 2 + 19

    def test_winner_score_2(self):

        data = [
            'Player 1:',
            '9',
            '2',
            '6',
            '3',
            '1',
            '',
            'Player 2:',
            '5',
            '8',
            '4',
            '7',
            '10'
        ]

        assert winner_score(data) == 291


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = winner_score(data)
    print(result)


if __name__ == '__main__':
    main()

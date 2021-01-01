#!/usr/bin/env python3

import sys


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


def winner_score(data):
    decks = parse_decks(data)

    while len(decks[0]) and len(decks[1]):
        head_1 = decks[0].pop(0)
        head_2 = decks[1].pop(0)

        if head_1 > head_2:
            decks[0].append(head_1)
            decks[0].append(head_2)
        else:
            decks[1].append(head_2)
            decks[1].append(head_1)

    winner = 0 if len(decks[0]) else 1

    result = sum([
        (len(decks[winner]) - i) * decks[winner][i]
        for i in range(len(decks[winner]))
    ])

    return result


class TestClass():

    def test_winner_score(self):

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

        assert winner_score(data) == 306


def main():
    data = [line.strip() for line in sys.stdin if len(line.strip())]
    result = winner_score(data)
    print(result)


if __name__ == '__main__':
    main()

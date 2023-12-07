#!/usr/bin/evn python3

import sys
from typing import List

CARD_STRENGTH = {
    card: -i
    for i, card in enumerate('AKQT98765432J')
}

HAND_STRENGTH = {
    (5, ): 6,
    (4, 1): 5,
    (3, 2): 4,
    (3, 1, 1): 3,
    (2, 2, 1): 2,
    (2, 1, 1, 1): 1,
    (1, 1, 1, 1, 1): 0
}


class Player:

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

        freq = {}
        jokers = 0

        for card in self.hand:
            if card == 'J':
                jokers += 1
            else:
                freq[card] = freq.get(card, 0) + 1

        values = sorted(freq.values(), reverse=True)

        if len(values) == 0:
            values = [0]

        values[0] += jokers

        self.hand_strength = HAND_STRENGTH[tuple(values)]

    def __lt__(self, other) -> bool:
        if self.hand_strength < other.hand_strength:
            return True
        if self.hand_strength == other.hand_strength:
            for i in range(len(self.hand)):
                if CARD_STRENGTH[self.hand[i]] < CARD_STRENGTH[other.hand[i]]:
                    return True
                if CARD_STRENGTH[self.hand[i]] > CARD_STRENGTH[other.hand[i]]:
                    return False
        return False


def parse_cards(data: List[str]) -> List[Player]:
    cards = []

    for line in data:
        hand, bid = line.split()
        cards.append(Player(hand, int(bid)))

    return cards


def total_score(data: List[str]) -> int:
    cards = parse_cards(data)
    score = sum(
        card.bid * (index + 1) for index, card in enumerate(sorted(cards))
    )
    return score


def test_total_score():
    data = [
        '32T3K 765',
        'T55J5 684',
        'KK677 28',
        'KTJJT 220',
        'QQQJA 483',
    ]
    assert total_score(data) == 5905


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = total_score(data)
    print(result)


if __name__ == '__main__':
    main()

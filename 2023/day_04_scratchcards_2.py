#!/usr/bin/env python3

import sys
from typing import Iterable, List, Set
from dataclasses import dataclass


@dataclass
class Card:
    win_set: Set[int]
    numbers: List[int]
    instances: int

    @classmethod
    def from_string(cls, line: str):
        left, right = line.split(': ')[1].split(' | ')
        win_set = set(int(value) for value in left.split() if len(value))
        numbers = [int(value) for value in right.split() if len(value)]
        return cls(win_set, numbers, 1)

    def calc_win_cards(self):
        return sum(1 for number in self.numbers if number in self.win_set)


def total_cards(data: Iterable[str]):
    cards = [Card.from_string(line) for line in data]
    for index, card in enumerate(cards):
        for i in range(card.calc_win_cards()):
            if index + i + 1 >= len(cards):
                continue
            cards[index + i + 1].instances += card.instances
    return sum(card.instances for card in cards)


def test_total_cards():
    data = [
        'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
        'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
        'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
        'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
        'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
        'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
    ]
    assert total_cards(data) == 30


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = total_cards(data)
    print(result)


if __name__ == '__main__':
    main()

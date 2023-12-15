#!/usr/bin/env python3

import sys
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Lens:
    label: str
    value: int
    prev: Optional['Lens'] = None
    next: Optional['Lens'] = None


class Box:

    def __init__(self):
        self.head = None
        self.tail = None
        self.map = {}

    def add(self, lens: Lens):
        if lens.label in self.map:
            self.map[lens.label].value = lens.value
            return

        if self.tail:
            lens.prev = self.tail
            self.tail.next = lens
        else:
            self.head = lens

        self.tail = lens
        self.map[lens.label] = lens

    def remove(self, label: str):
        if label not in self.map:
            return

        lens = self.map[label]
        del self.map[label]

        left, right = lens.prev, lens.next

        if left is None and right is None:
            self.head = None
            self.tail = None
        elif left is None:
            right.prev = None
            self.head = right
        elif right is None:
            left.next = None
            self.tail = left
        else:
            left.next = right
            right.prev = left

    def score(self) -> int:
        result, i = 0, 0
        lens = self.head

        while lens:
            result += lens.value * (i + 1)
            lens = lens.next
            i += 1

        return result


def seq_score(seq: str) -> int:
    current_value = 0

    for char in seq:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


def total_score(data: List[str], size=256) -> int:
    boxes = [Box() for i in range(size)]

    for item in data:
        if '=' in item:
            label, value = item.split('=')
            box_number = seq_score(label)
            boxes[box_number].add(Lens(label, int(value)))
        elif '-' in item:
            label = item.rstrip('-')
            box_number = seq_score(label)
            boxes[box_number].remove(label)

    result = 0

    for i, box in enumerate(boxes):
        result += box.score() * (i + 1)

    return result


def test_seq_score():
    assert seq_score('HASH') == 52


def test_total_score():
    data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    assert total_score(data.split(',')) == 145


def main():
    data = sys.stdin.read().rstrip('\n')
    result = total_score(data.split(','))
    print(result)


if __name__ == '__main__':
    main()

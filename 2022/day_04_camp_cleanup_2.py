#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Segment:
    left: int
    right: int

    @classmethod
    def from_string(cls, line: str) -> 'Segment':
        left, right = line.split('-')
        return cls(int(left), int(right))

    def overlaps(self, other: 'Segment') -> bool:
        return max(self.left, other.left) <= min(self.right, other.right)


def overlap_count(data: Iterable[str]) -> int:
    result = 0

    for line in data:
        part_1, part_2 = line.split(',')

        seg_1 = Segment.from_string(part_1)
        seg_2 = Segment.from_string(part_2)

        if seg_1.overlaps(seg_2):
            result += 1

    return result


def test_overlap_count():
    data = [
        '2-4,6-8',
        '2-3,4-5',
        '5-7,7-9',
        '2-8,3-7',
        '6-6,4-6',
        '2-6,4-8',
    ]

    assert overlap_count(data) == 4


def main() -> None:
    data = sys.stdin
    result = overlap_count(data)
    print(result)


if __name__ == '__main__':
    main()

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

    def contains(self, other: 'Segment') -> bool:
        return self.left <= other.left and self.right >= other.right


def full_overlap_count(data: Iterable[str]) -> int:
    result = 0

    for line in data:
        part_1, part_2 = line.split(',')

        seg_1 = Segment.from_string(part_1)
        seg_2 = Segment.from_string(part_2)

        if seg_1.contains(seg_2) or seg_2.contains(seg_1):
            result += 1

    return result


def test_full_overlap_count():
    data = [
        '2-4,6-8',
        '2-3,4-5',
        '5-7,7-9',
        '2-8,3-7',
        '6-6,4-6',
        '2-6,4-8',
    ]

    assert full_overlap_count(data) == 2


def main() -> None:
    data = sys.stdin
    result = full_overlap_count(data)
    print(result)


if __name__ == '__main__':
    main()

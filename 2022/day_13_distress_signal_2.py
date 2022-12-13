#!/usr/bin/env python3

import sys
import json
from typing import Iterable, List, Any, Optional


def is_right_order(left: List[Any], right: List[Any]) -> Optional[bool]:
    iter_left = iter(left)
    iter_right = iter(right)

    while True:
        item_left = next(iter_left, None)
        item_right = next(iter_right, None)

        if item_left is None and item_right is None:
            return None

        if item_left is None:
            return True

        if item_right is None:
            return False

        if isinstance(item_left, int) and isinstance(item_right, int):
            if item_left < item_right:
                return True
            if item_left > item_right:
                return False
            if item_right == item_left:
                continue

        if isinstance(item_left, int):
            item_left = [item_left]

        if isinstance(item_right, int):
            item_right = [item_right]

        value = is_right_order(item_left, item_right)

        if value is not None:
            return value


class Packet:

    def __init__(self, line: str, is_special: bool = False):
        self.value = json.loads(line)
        self.is_special = is_special

    def __lt__(self, other) -> bool:
        return True if is_right_order(self.value, other.value) else False


def decoder_key(data: Iterable[str]) -> int:
    packets = [Packet(line) for line in data if line.strip()]

    packets.append(Packet('[[2]]', True))
    packets.append(Packet('[[6]]', True))

    packets.sort()

    positions = [
        index + 1 for index, packet in enumerate(packets) if packet.is_special
    ]

    return positions[0] * positions[1]


def test_decoder_key():
    data = [
        '[1,1,3,1,1]',
        '[1,1,5,1,1]',
        '',
        '[[1],[2,3,4]]',
        '[[1],4]',
        '',
        '[9]',
        '[[8,7,6]]',
        '',
        '[[4,4],4,4]',
        '[[4,4],4,4,4]',
        '',
        '[7,7,7,7]',
        '[7,7,7]',
        '',
        '[]',
        '[3]',
        '',
        '[[[]]]',
        '[[]]',
        '',
        '[1,[2,[3,[4,[5,6,7]]]],8,9]',
        '[1,[2,[3,[4,[5,6,0]]]],8,9]'
    ]

    assert decoder_key(data) == 140


def main():
    data = sys.stdin
    result = decoder_key(data)
    print(result)


if __name__ == '__main__':
    main()

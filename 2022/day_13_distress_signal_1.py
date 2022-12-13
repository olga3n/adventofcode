#!/usr/bin/env python3

import sys
import json
from typing import Iterable, List, Any, Tuple, Optional


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


def build_pairs(data: Iterable[str]) -> Iterable[Tuple[List[Any], List[Any]]]:
    buf = []

    for line in data:
        if not line.strip():
            continue

        buf.append(line)

        if len(buf) == 2:
            yield json.loads(buf[0]), json.loads(buf[1])
            buf = []


def right_order_pairs(data: Iterable[str]) -> int:
    return sum(
        index + 1 for index, pair in enumerate(build_pairs(data))
        if is_right_order(pair[0], pair[1])
    )


def test_right_order_pairs():
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

    assert right_order_pairs(data) == 13


def main():
    data = sys.stdin
    result = right_order_pairs(data)
    print(result)


if __name__ == '__main__':
    main()

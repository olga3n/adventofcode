#!/usr/bin/env python3

import sys
from dataclasses import dataclass
from collections import deque


@dataclass
class Fragment:
    value: int
    start: int
    length: int


def parse_fragments(line: str) -> tuple[list[Fragment], list[Fragment]]:
    full_fragments = []
    empty_fragments = []

    value = 0
    start = 0

    for i, symbol in enumerate(line):
        length = int(symbol)

        if i % 2 == 0:
            full_fragments.append(Fragment(value, start, length))
            value += 1
        elif length > 0:
            empty_fragments.append(Fragment(-1, start, length))

        start += length

    return full_fragments, empty_fragments


def fragmenter_checksum(
    full_fragments: list[Fragment], empty_fragments: list[Fragment]
) -> int:
    empty_queue = deque(empty_fragments)
    full_queue = deque(full_fragments)

    while len(empty_queue) > 0:
        next_empty = empty_queue.popleft()
        next_full = full_queue.pop()

        if next_full.start < next_empty.start:
            full_queue.append(next_full)
            break

        if next_empty.length == next_full.length:
            next_full.start = next_empty.start
            full_queue.appendleft(next_full)
        elif next_empty.length > next_full.length:
            next_full.start = next_empty.start
            full_queue.appendleft(next_full)
            next_empty.length -= next_full.length
            next_empty.start += next_full.length
            empty_queue.appendleft(next_empty)
        else:
            full_fragment = Fragment(
                next_full.value,
                next_empty.start,
                next_empty.length,
            )
            full_queue.appendleft(full_fragment)
            next_full.length -= next_empty.length
            full_queue.append(next_full)

    result = 0

    for fragment in full_queue:
        for i in range(fragment.start, fragment.start + fragment.length):
            result += i * fragment.value

    return result


def test_fragmenter_checksum():
    line = '2333133121414131402'
    assert 1928 == fragmenter_checksum(*parse_fragments(line))


def main():
    line = sys.stdin.readline().rstrip()
    result = fragmenter_checksum(*parse_fragments(line))
    print(result)


if __name__ == '__main__':
    main()

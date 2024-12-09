#!/usr/bin/env python3

import sys
from dataclasses import dataclass


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
    empty_lst = empty_fragments
    full_lst: list[Fragment] = []

    for next_full in reversed(full_fragments):
        new_empty_lst: list[Fragment] = []
        inserted = False

        for next_empty in empty_lst:
            if inserted or next_empty.start > next_full.start:
                new_empty_lst.append(next_empty)
            elif next_empty.length == next_full.length:
                next_full.start = next_empty.start
                full_lst.append(next_full)
                inserted = True
            elif next_empty.length > next_full.length:
                next_full.start = next_empty.start
                full_lst.append(next_full)
                next_empty.length -= next_full.length
                next_empty.start += next_full.length
                new_empty_lst.append(next_empty)
                inserted = True
            else:
                new_empty_lst.append(next_empty)

        if not inserted:
            full_lst.append(next_full)

        empty_lst = new_empty_lst

    result = 0

    for fragment in full_lst:
        for i in range(fragment.start, fragment.start + fragment.length):
            result += i * fragment.value

    return result


def test_fragmenter_checksum():
    line = '2333133121414131402'
    assert 2858 == fragmenter_checksum(*parse_fragments(line))


def main():
    line = sys.stdin.readline().rstrip()
    result = fragmenter_checksum(*parse_fragments(line))
    print(result)


if __name__ == '__main__':
    main()

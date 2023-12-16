#!/usr/bin env python3

import sys
from typing import List, Tuple

NEXT_DIFF = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0)
}

ROTATIONS = {
    ('>', '|'): ('^', 'v'),
    ('<', '|'): ('^', 'v'),
    ('v', '-'): ('<', '>'),
    ('^', '-'): ('<', '>'),
    ('>', '/'): ('^',),
    ('<', '/'): ('v',),
    ('v', '/'): ('<',),
    ('^', '/'): ('>',),
    ('>', '\\'): ('v',),
    ('<', '\\'): ('^',),
    ('v', '\\'): ('>',),
    ('^', '\\'): ('<',),
}


def energized_tiles(
    data: List[str], start_view: str, start_pos: Tuple[int, int]
) -> int:
    visited = {}

    symbol = data[start_pos[0]][start_pos[1]]
    beams = [
        (start_view, start_pos)
        for view in ROTATIONS.get((start_view, symbol), (start_view,))
    ]

    while len(beams):
        new_beams = []

        for view, (x, y) in beams:
            if (x, y) in visited:
                if view in visited[(x, y)]:
                    continue
                else:
                    visited[(x, y)].add(view)
            else:
                visited[(x, y)] = {view}
            dx, dy = NEXT_DIFF[view]
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < len(data) and 0 <= new_y < len(data[0])):
                continue
            for new_view in ROTATIONS.get((view, data[new_x][new_y]), (view,)):
                new_beams.append((new_view, (new_x, new_y)))

        beams = new_beams

    return len(visited)


def max_energized_tiles(data: List[str]) -> int:
    result = 0

    for i in range(0, len(data)):
        result = max(result, energized_tiles(data, '>', (i, 0)))
        result = max(result, energized_tiles(data, '<', (i, len(data[0]) - 1)))

    for j in range(0, len(data[0])):
        result = max(result, energized_tiles(data, 'v', (0, j)))
        result = max(result, energized_tiles(data, '^', (len(data) - 1, j)))

    return result


def test_max_energized_tiles():
    data = [
        r'.|...\....',
        r'|.-.\.....',
        '.....|-...',
        '........|.',
        '..........',
        '.........\\',
        '..../.\\\\..',
        '.-.-/..|..',
        '.|....-|.\\',
        '..//.|....',
    ]
    assert max_energized_tiles(data) == 51


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = max_energized_tiles(data)
    print(result)


if __name__ == '__main__':
    main()

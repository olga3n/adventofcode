#!/usr/bin env python3

import sys
from typing import List

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


def energized_tiles(data: List[str]) -> int:
    visited = {}
    beams = [
        (view, (0, 0)) for view in ROTATIONS.get(('>', data[0][0]), ('>',))
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


def test_energized_tiles():
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
    assert energized_tiles(data) == 46


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = [line for line in data if len(line)]
    result = energized_tiles(data)
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
from collections import deque


NUMERIC_KEYPAD = (
    ('7', '8', '9'),
    ('4', '5', '6'),
    ('1', '2', '3'),
    ('G', '0', 'A'),
)

DIRECTIONAL_KEYPAD = (
    ('G', '^', 'A'),
    ('<', 'v', '>'),
)

MOVES = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}


def all_shortest_paths_for_keypad(keypad):
    shortest_paths = {}
    pairs = []

    for x in range(len(keypad)):
        for y in range(len(keypad[0])):
            for xx in range(len(keypad)):
                for yy in range(len(keypad[0])):
                    if (x, y) == (xx, yy):
                        continue
                    pairs.append(((x, y), (xx, yy)))

    for start, end in pairs:
        queue = deque([(start, '')])
        visited = set()

        while queue:
            pos, path = queue.popleft()

            if pos == end:
                symbol_from = keypad[start[0]][start[1]]
                symbol_to = keypad[end[0]][end[1]]
                key = (symbol_from, symbol_to)
                if key not in shortest_paths:
                    shortest_paths[key] = [path]
                elif len(shortest_paths[key][0]) < len(path):
                    break
                else:
                    shortest_paths[key].append(path)

            if len(path) > 0 and (pos, path[-1]) in visited:
                continue

            if len(path) > 0:
                visited.add((pos, path[-1]))

            for next_move, (dx, dy) in MOVES.items():
                x = pos[0] + dx
                y = pos[1] + dy

                if not 0 <= x < len(keypad):
                    continue

                if not 0 <= y < len(keypad[x]):
                    continue

                if keypad[x][y] == 'G':
                    continue

                if keypad[x][y] != 'A' or keypad[end[0]][end[1]] == 'A':
                    queue.append(((x, y), path + next_move))

    return shortest_paths


def seq_options(lines: list[str], paths: dict) -> list[str]:
    result = []

    for line in lines:
        line_options = []
        line_seq_options = ['']
        prev_symbol = 'A'

        for symbol in line:
            if prev_symbol == symbol:
                new_seq_options = []
                for value in line_seq_options:
                    new_seq_options.append(value + 'A')
                line_seq_options = new_seq_options
                continue

            line_options.append(paths[(prev_symbol, symbol)])
            new_seq_options = []

            for prefix in line_seq_options:
                for suffix in paths[(prev_symbol, symbol)]:
                    new_seq_options.append(prefix + suffix + 'A')

            line_seq_options = new_seq_options
            prev_symbol = symbol

        result.extend(line_seq_options)

    return list(set(result))


def shortest_seq_len(line: str) -> int:
    paths_1 = all_shortest_paths_for_keypad(NUMERIC_KEYPAD)
    paths_2 = all_shortest_paths_for_keypad(DIRECTIONAL_KEYPAD)

    options = seq_options([line], paths_1)
    opt_len = min(len(x) for x in options)
    options = [x for x in options if len(x) == opt_len]

    options = seq_options(options, paths_2)
    opt_len = min(len(x) for x in options)
    options = [x for x in options if len(x) == opt_len]

    options = seq_options(options, paths_2)
    opt_len = min(len(x) for x in options)
    options = [x for x in options if len(x) == opt_len]

    return opt_len


def complexity_value(lines: list[str]) -> int:
    result = 0

    for line in lines:
        numeric_part = ''.join(
            [symbol for symbol in line if symbol.isdigit()]
        )
        result += shortest_seq_len(line) * int(numeric_part)

    return result


def test_shortest_seq_len():
    line = '029A'
    assert 68 == shortest_seq_len(line)


def test_complexity_value():
    lines = [
        '029A',
        '980A',
        '179A',
        '456A',
        '379A',
    ]
    assert 126384 == complexity_value(lines)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = complexity_value(lines)
    print(result)


if __name__ == '__main__':
    main()

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

SEQ_COST = {
    ('^', 'v'): 1,
    ('<', 'v'): 1,
    ('>', 'v'): 1,
    ('<', '>'): 2,
    ('<', '^'): 2,
    ('>', '^'): 2,
    ('<', 'A'): 3,
    ('>', 'A'): 1,
    ('A', '^'): 1,
    ('A', 'v'): 2,
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


def partition(line: str) -> list[str]:
    seq = []
    next_part = ''

    for symbol in line:
        next_part += symbol
        if symbol == 'A':
            seq.append(next_part)
            next_part = ''

    return seq


def partition_freq(line: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for item in partition(line):
        freq[item] = freq.get(item, 0) + 1
    return freq


def seq_score(line: str) -> int:
    result = 0
    prev_symbol = ''

    for symbol in line:
        if symbol < prev_symbol:
            key = (symbol, prev_symbol)
        else:
            key = (prev_symbol, symbol)
        result += SEQ_COST.get(key, 0)
        prev_symbol = symbol

    return result


def build_cache(options: list[str], paths: dict) -> dict[str, list[str]]:
    cache = {}
    tmp_options = options

    while len(tmp_options) > 0:
        seq = []
        for x in tmp_options:
            seq.extend(partition(x))

        tmp_options = []

        for part in seq:
            if part in cache:
                continue

            part_options = seq_options([part], paths)
            opt_len = min(len(x) for x in part_options)
            part_options = [x for x in part_options if len(x) == opt_len]
            cache[part] = part_options
            tmp_options.extend(part_options)

    for k, v_lst in cache.items():
        best_score = -1
        new_v_lst = []

        for x in v_lst:
            score = seq_score(x)
            if best_score == -1:
                new_v_lst.append(x)
                best_score = score
            elif score < best_score:
                new_v_lst = [x]
                best_score = score
            elif score == best_score:
                new_v_lst.append(x)

        cache[k] = new_v_lst

    return cache


def best_freq_options(
    freq_options: list[dict[str, int]],
) -> list[dict[str, int]]:
    min_len = -1
    for freq in freq_options:
        curr_len = sum(len(k) * v for k, v in freq.items())
        if curr_len < min_len or min_len == -1:
            min_len = curr_len

    freq_options = [
        freq
        for freq in freq_options
        if sum(len(k) * v for k, v in freq.items()) == min_len
    ]

    uniq_options = set(
        tuple(sorted(freq.items())) for freq in freq_options
    )
    return [dict(freq) for freq in uniq_options]


def process_extra_levels(
    options: list[str], cache: dict[str, list[str]], levels: int = 25,
) -> list[dict[str, int]]:

    cache_with_freq = {}
    for k, v_lst in cache.items():
        cache_with_freq[k] = [partition_freq(v) for v in v_lst]

    freq_options = []
    for option in options:
        freq = partition_freq(option)
        freq_options.append(freq)

    for _ in range(levels):
        new_freq_options = []

        for freq_opt in freq_options:
            buf: list[dict[str, int]] = [{}]
            for k_prev, v_prev in freq_opt.items():
                new_buf = []
                for freq in cache_with_freq[k_prev]:
                    for tmp_freq in buf:
                        tmp = tmp_freq.copy()
                        for k_new, v_new in freq.items():
                            tmp[k_new] = tmp.get(k_new, 0) + v_new * v_prev
                        new_buf.append(tmp)
                buf = new_buf

            new_freq_options.extend(buf)

        freq_options = best_freq_options(new_freq_options)

    return freq_options


def shortest_seq_len(line: str, levels: int = 25) -> int:
    paths_1 = all_shortest_paths_for_keypad(NUMERIC_KEYPAD)
    paths_2 = all_shortest_paths_for_keypad(DIRECTIONAL_KEYPAD)

    options = seq_options([line], paths_1)
    opt_len = min(len(x) for x in options)
    options = [x for x in options if len(x) == opt_len]

    cache = build_cache(options, paths_2)
    freq_options = process_extra_levels(options, cache, levels)

    best_score = -1

    for freq in freq_options:
        score = sum([len(k) * v for k, v in freq.items()])
        if best_score == -1 or best_score < score:
            best_score = score

    return best_score


def complexity_value(lines: list[str], levels: int = 25) -> int:
    result = 0

    for line in lines:
        numeric_part = ''.join(
            [symbol for symbol in line if symbol.isdigit()]
        )
        result += shortest_seq_len(line, levels) * int(numeric_part)

    return result


def test_complexity_value():
    lines = [
        '029A',
        '980A',
        '179A',
        '456A',
        '379A',
    ]
    assert 126384 == complexity_value(lines, levels=2)


def main():
    lines = [line.rstrip() for line in sys.stdin]
    result = complexity_value(lines)
    print(result)


if __name__ == '__main__':
    main()

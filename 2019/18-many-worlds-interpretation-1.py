#!/usr/bin/env python3

import sys
from collections import deque


def field_successors(data, pos):
    successors = []

    ii, jj = pos

    if ii > 0 and data[ii - 1][jj] != '#':
        successors.append((ii - 1, jj))

    if ii < len(data) - 1 and data[ii + 1][jj] != '#':
        successors.append((ii + 1, jj))

    if jj > 0 and data[ii][jj - 1] != '#':
        successors.append((ii, jj - 1))

    if jj < len(data[ii]) - 1 and data[ii][jj + 1] != '#':
        successors.append((ii, jj + 1))

    return successors


def bfs_paths(data, pos):
    paths = {}

    state = (pos, set(), 0)

    first_key = data[pos[0]][pos[1]]

    used = set()
    used.add(pos)

    q = deque([state])

    while len(q):
        pos, keys, path_len = q.popleft()

        for s_pos in field_successors(data, pos):
            if s_pos not in used:
                used.add(s_pos)

                ii, jj = s_pos

                if 'A' <= data[ii][jj] <= 'Z':
                    if data[ii][jj].lower() in keys:
                        new_state = (s_pos, keys, path_len + 1)
                    else:
                        new_keys = set(keys)
                        new_keys.add(data[ii][jj].lower())

                        new_state = (s_pos, new_keys, path_len + 1)

                    q.append(new_state)
                else:
                    new_state = (s_pos, keys, path_len + 1)
                    q.append(new_state)

                    if 'a' <= data[ii][jj] <= 'z' and \
                            data[ii][jj] not in keys:
                        paths[data[ii][jj]] = (keys, path_len + 1)
    return paths


def reachable(item, keys):
    return keys.union(item[0]) == keys


def shortest_path(data):
    start_pos = (-1, -1)
    all_keys = set()
    keys_pos = {}

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '@':
                start_pos = (i, j)
            if 'a' <= data[i][j] <= 'z':
                all_keys.add(data[i][j])
                keys_pos[data[i][j]] = (i, j)

    paths = {}

    paths['@'] = bfs_paths(data, start_pos)

    for k, pos in keys_pos.items():
        paths[k] = bfs_paths(data, pos)

    cache = {}

    s = deque()

    for key, item in paths['@'].items():
        if key in all_keys and reachable(item, set()):
            state = (key, all_keys - {key}, {key})
            s.append(state)

        cache[(key, tuple())] = 0

    while len(s):
        curr_key, needed_keys, collected_keys = s[0]

        appended = 0

        for key, item in paths[curr_key].items():
            if key in needed_keys and reachable(item, collected_keys):
                cache_item = (key, tuple(sorted(needed_keys - {key})))

                if cache_item not in cache:
                    new_keys = set(collected_keys)
                    new_keys.add(key)

                    state = (key, needed_keys - {key}, new_keys)

                    s.appendleft(state)
                    appended += 1
                else:
                    new_cache_item = (curr_key, tuple(sorted(needed_keys)))

                    if new_cache_item not in cache:
                        cache[new_cache_item] = cache[cache_item] + item[1]
                    else:
                        cache[new_cache_item] = min(
                            cache[new_cache_item], cache[cache_item] + item[1])

        if appended == 0:
            s.popleft()

    min_dist = 100500

    for k, v in cache.items():

        if len(k[1]) == len(all_keys) - 1 and \
                k[0] in paths['@'] and len(paths['@'][k[0]][0]) == 0:
            min_dist = min(min_dist, v + paths['@'][k[0]][1])

    return min_dist


class TestClass:
    def test_shortest_path_0(self):
        data = [
            '#########',
            '#b.A.@.a#',
            '#########']

        assert shortest_path(data) == 8

    def test_shortest_path_1(self):
        data = [
            '########################',
            '#f.D.E.e.C.b.A.@.a.B.c.#',
            '######################.#',
            '#d.....................#',
            '########################']

        assert shortest_path(data) == 86

    def test_shortest_path_2(self):
        data = [
            '########################',
            '#...............b.C.D.f#',
            '#.######################',
            '#.....@.a.B.c.d.A.e.F.g#',
            '########################']

        assert shortest_path(data) == 132

    def test_shortest_path_3(self):
        data = [
            '#################',
            '#i.G..c...e..H.p#',
            '########.########',
            '#j.A..b...f..D.o#',
            '########@########',
            '#k.E..a...g..B.n#',
            '########.########',
            '#l.F..d...h..C.m#',
            '#################']

        assert shortest_path(data) == 136

    def test_shortest_path_4(self):
        data = [
            '########################',
            '#@..............ac.GI.b#',
            '###d#e#f################',
            '###A#B#C################',
            '###g#h#i################',
            '########################']

        assert shortest_path(data) == 81


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.strip() for x in data]

    result = shortest_path(data)

    print(result)

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
    robots = []
    all_keys = set()
    keys_pos = {}

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '@':
                robots.append((i, j))
            if 'a' <= data[i][j] <= 'z':
                all_keys.add(data[i][j])
                keys_pos[data[i][j]] = (i, j)

    paths = {}

    for i, robot_pos in enumerate(robots):
        paths[str(i)] = bfs_paths(data, robot_pos)

    for k, pos in keys_pos.items():
        paths[k] = bfs_paths(data, pos)

    cache = {}

    s = deque()

    robots_fig = tuple([str(i) for i in range(len(robots))])

    state = (robots_fig, all_keys, set())

    s.append(state)

    while len(s):
        robots_fig, needed_keys, collected_keys = s[0]

        appended = 0

        for i, curr_key in enumerate(robots_fig):
            for key, item in paths[curr_key].items():
                if key in needed_keys and reachable(item, collected_keys):
                    tmp_robots_fig = list(robots_fig)
                    tmp_robots_fig[i] = key
                    tmp_robots_fig = tuple(tmp_robots_fig)

                    cache_item = (
                        tmp_robots_fig, tuple(sorted(needed_keys - {key})))

                    if len(cache_item[1]) == 0:
                        cache[cache_item] = 0

                    if cache_item not in cache:
                        new_keys = set(collected_keys)
                        new_keys.add(key)

                        state = (tmp_robots_fig, needed_keys - {key}, new_keys)

                        s.appendleft(state)
                        appended += 1
                    else:
                        new_cache_item = (
                            robots_fig, tuple(sorted(needed_keys)))

                        if new_cache_item not in cache:
                            cache[new_cache_item] = cache[cache_item] + item[1]
                        else:
                            cache[new_cache_item] = min(
                                cache[new_cache_item],
                                cache[cache_item] + item[1])

        if appended == 0:
            s.popleft()

    robots_fig = tuple([str(i) for i in range(len(robots))])

    min_dist = cache[(robots_fig, tuple(sorted(all_keys)))]

    return min_dist


class TestClass:
    def test_shortest_path_0(self):
        data = [
            '#######',
            '#a.#Cd#',
            '##@#@##',
            '#######',
            '##@#@##',
            '#cB#Ab#',
            '#######']

        assert shortest_path(data) == 8

    def test_shortest_path_1(self):
        data = [
            '###############',
            '#d.ABC.#.....a#',
            '######@#@######',
            '###############',
            '######@#@######',
            '#b.....#.....c#',
            '###############']

        assert shortest_path(data) == 24

    def test_shortest_path_2(self):
        data = [
            '#############',
            '#DcBa.#.GhKl#',
            '#.###@#@#I###',
            '#e#d#####j#k#',
            '###C#@#@###J#',
            '#fEbA.#.FgHi#',
            '#############']

        assert shortest_path(data) == 32

    def test_shortest_path_3(self):
        data = [
            '#############',
            '#g#f.D#..h#l#',
            '#F###e#E###.#',
            '#dCba@#@BcIJ#',
            '#############',
            '#nK.L@#@G...#',
            '#M###N#H###.#',
            '#o#m..#i#jk.#',
            '#############']

        assert shortest_path(data) == 72


if __name__ == '__main__':
    data = sys.stdin.readlines()
    data = [x.strip() for x in data]

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '@':
                start_pos = (i, j)

    i, j = start_pos

    data[i - 1] = data[i - 1][:j - 1] + '@#@' + data[i - 1][j + 2:]
    data[i] = data[i][:j - 1] + '###' + data[i][j + 2:]
    data[i + 1] = data[i + 1][:j - 1] + '@#@' + data[i + 1][j + 2:]

    result = shortest_path(data)

    print(result)

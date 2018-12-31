#!/usr/bin/env python3

import sys

import collections

import unittest
import textwrap


def build_graph(data, pos, i, graph):

    first_pos = pos

    while i < len(data):

        if data[i] in ['N', 'S', 'W', 'E']:

            if data[i] == 'N':
                new_pos = (pos[0] + 1, pos[1])
            elif data[i] == 'S':
                new_pos = (pos[0] - 1, pos[1])
            elif data[i] == 'E':
                new_pos = (pos[0], pos[1] + 1)
            elif data[i] == 'W':
                new_pos = (pos[0], pos[1] - 1)

            if pos in graph:
                graph[pos].append(new_pos)
            else:
                graph[pos] = [new_pos]

            if new_pos in graph:
                graph[new_pos].append(pos)
            else:
                graph[new_pos] = [pos]

            pos = new_pos

            i += 1

        elif data[i] == '(':
            _, i = build_graph(data, pos, i + 1, graph)

        elif data[i] == '|':
            _, i = build_graph(data, first_pos, i + 1, graph)
            break

        elif data[i] == ')':
            i += 1
            break

    return pos, i


def max_path(data):

    graph = {}

    _, _ = build_graph(data[1:-1], (0, 0), 0, graph)

    q = collections.deque()

    q.append((0, 0, 0))

    len_dict = {}

    while len(q):
        item = q.popleft()

        v0 = (item[0], item[1])
        curr_len = item[2]

        if v0 in len_dict:
            continue

        len_dict[v0] = curr_len

        for v1 in graph[v0]:
            if v1 not in len_dict:
                q.append((v1[0], v1[1], curr_len + 1))

    result = max(len_dict.values())

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            ^WNE$
        """).rstrip()

        self.assertEqual(max_path(data), 3)

    def test_1(self):
        data = textwrap.dedent("""\
            ^ENWWW(NEEE|SSE(EE|N))$
        """).rstrip()

        self.assertEqual(max_path(data), 10)

    def test_2(self):
        data = textwrap.dedent("""\
            ^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
        """).rstrip()

        self.assertEqual(max_path(data), 18)

    def test_3(self):
        data = textwrap.dedent("""\
            ^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
        """).rstrip()

        self.assertEqual(max_path(data), 23)

    def test_4(self):
        data = textwrap.dedent("""\
            ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
        """).rstrip()

        self.assertEqual(max_path(data), 31)


if __name__ == '__main__':
    data = sys.stdin.readlines()[0].rstrip()

    v = max_path(data)

    print(v)

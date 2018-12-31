#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def parse_data(data):
    deps_count = np.full(26, np.inf)
    next_steps = {}

    for line in data:
        prs = line.split(' ')

        w1 = prs[1]
        w2 = prs[7]

        if w1 not in next_steps:
            next_steps[w1] = [w2]
        else:
            next_steps[w1].append(w2)

        if deps_count[ord(w1) - ord('A')] == np.inf:
            deps_count[ord(w1) - ord('A')] = 0

        if deps_count[ord(w2) - ord('A')] == np.inf:
            deps_count[ord(w2) - ord('A')] = 0

        deps_count[ord(w2) - ord('A')] += 1

    return deps_count, next_steps


def steps_order(data):
    deps_count, next_steps = parse_data(data)

    result = ''

    for i in range(len(next_steps.keys()) + 1):
        ind = np.argmin(deps_count)

        w = chr(ind + ord('A'))

        result += w

        if w in next_steps:
            for item in next_steps[w]:
                deps_count[ord(item) - ord('A')] -= 1

        deps_count[ind] = np.inf

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            Step C must be finished before step A can begin.
            Step C must be finished before step F can begin.
            Step A must be finished before step B can begin.
            Step A must be finished before step D can begin.
            Step B must be finished before step E can begin.
            Step D must be finished before step E can begin.
            Step F must be finished before step E can begin.
            """).split("\n")

        data = [x for x in data if len(x)]

        self.assertEqual(steps_order(data), 'CABDFE')


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = steps_order(data)

    print(v)

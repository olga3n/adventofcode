#!/usr/bin/env python3

import sys
import re

import numpy as np

import unittest
import textwrap


def parse_data(data):

    data = sorted(data)

    guard_id = -1
    guard_ind = -1

    guards = []

    events = np.zeros((len(data), 3))

    for i, item in enumerate(data):
        dt_prs = item.split(']')[0].split(' ')[1].split(':')

        dt = int(dt_prs[1])

        if 'Guard' in item:
            guard_id = int(item.split('#')[1].split(' ')[0])

            if guard_id not in guards:
                guard_ind = len(guards)
                guards.append(guard_id)
            else:
                guard_ind = guards.index(guard_id)

        elif 'falls asleep' in item:
            events[i][0] = guard_ind
            events[i][1] = dt
            events[i][2] = 1

        elif 'wakes up' in item:
            events[i][0] = guard_ind
            events[i][1] = dt
            events[i][2] = -1

    return guards, events


def strategy_1(events, n):
    m = np.zeros((n, 60))

    for item in events:
        m[int(item[0])][int(item[1])] += item[2]

    max_sleep_time = 0
    max_id = -1
    max_min = 0

    for i in range(n):
        sleep_time = 0
        max_intersection = 0
        max_intersection_min = 0

        for j in range(60):
            if j > 0:
                m[i][j] += m[i][j - 1]

            sleep_time += m[i][j]

            if m[i][j] > max_intersection:
                max_intersection = m[i][j]
                max_intersection_min = j

        if sleep_time > max_sleep_time:
            max_sleep_time = sleep_time
            max_id = i
            max_min = max_intersection_min

    return max_id, max_min


def strategy_1_solution(data):

    guards, events = parse_data(data)

    guard_ind, m = strategy_1(events, len(guards))

    return guards[int(guard_ind)] * m


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = textwrap.dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:05] falls asleep
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-02 00:40] falls asleep
            [1518-11-02 00:50] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-03 00:24] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-05 00:55] wakes up
            """).split("\n")

        data = [x for x in data if len(x)]

        self.assertEqual(strategy_1_solution(data), 240)


if __name__ == '__main__':
    data = sys.stdin.readlines()

    data = [x.rstrip() for x in data]
    data = [x for x in data if len(x)]

    v = strategy_1_solution(data)

    print(v)

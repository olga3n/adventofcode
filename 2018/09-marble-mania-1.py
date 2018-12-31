#!/usr/bin/env python3

import sys

import unittest


class Node(object):

    def __init__(self, val, left, right):
        self.val = val

        self.left = left
        self.right = right


def high_score(data):
    prs = data.split(' ')

    players, last_ind = int(prs[0]), int(prs[6])

    node = Node(0, None, None)

    node.left = node
    node.right = node

    curr_node = node
    curr_player = 0

    score = [0] * players

    for i in range(1, last_ind + 1):

        if i % 23 != 0:
            left_node = curr_node.right
            right_node = curr_node.right.right

            new_node = Node(i, left_node, right_node)

            left_node.right = new_node
            right_node.left = new_node

            curr_node = new_node

        else:
            score[curr_player] += i

            del_node = curr_node

            for j in range(7):
                del_node = del_node.left

            left_node = del_node.left
            right_node = del_node.right

            score[curr_player] += del_node.val

            left_node.right = right_node
            right_node.left = left_node

            curr_node = right_node

        curr_player += 1
        curr_player = 0 if curr_player == players else curr_player

    result = max(score)

    return result


class TestMethods(unittest.TestCase):

    def test_0(self):
        data = """9 players; last marble is worth 25 points"""

        self.assertEqual(high_score(data), 32)

    def test_1(self):
        data = """10 players; last marble is worth 1618 points"""

        self.assertEqual(high_score(data), 8317)

    def test_2(self):
        data = """13 players; last marble is worth 7999 points"""

        self.assertEqual(high_score(data), 146373)

    def test_3(self):
        data = """17 players; last marble is worth 1104 points"""

        self.assertEqual(high_score(data), 2764)

    def test_4(self):
        data = """21 players; last marble is worth 6111 points"""

        self.assertEqual(high_score(data), 54718)

    def test_5(self):
        data = """30 players; last marble is worth 5807 points"""

        self.assertEqual(high_score(data), 37305)


if __name__ == '__main__':
    data = ''.join(sys.stdin.readlines()).rstrip()

    v = high_score(data)

    print(v)

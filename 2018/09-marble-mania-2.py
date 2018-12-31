#!/usr/bin/env python3

import sys


class Node(object):

    def __init__(self, val, left, right):
        self.val = val

        self.left = left
        self.right = right


def high_score(data):
    prs = data.split(' ')

    players, last_ind = int(prs[0]), int(prs[6]) * 100

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


if __name__ == '__main__':
    data = ''.join(sys.stdin.readlines()).rstrip()

    v = high_score(data)

    print(v)

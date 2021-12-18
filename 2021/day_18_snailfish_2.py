#!/usr/bin/env python3

import sys
import json
from typing import List


class Node:
    def __init__(self, left=None, right=None, value=None, parent=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent

    def __str__(self):
        if self.value is not None:
            return str(self.value)

        return "[%s,%s]" % (str(self.left), str(self.right))


def build_tree(data: str):
    if isinstance(data, int):
        return Node(value=data)

    n1 = build_tree(data[0])
    n2 = build_tree(data[1])

    tree = Node(left=n1, right=n2)

    n1.parent = tree
    n2.parent = tree

    return tree


def parse_tree(data: str) -> Node:
    return build_tree(json.loads(data))


def add_left(tree: Node, value: int) -> None:
    while tree.parent is not None:
        if tree.parent.right == tree:
            break
        tree = tree.parent

    tree = tree.parent

    if tree is None:
        return

    tree = tree.left

    while tree.value is None:
        tree = tree.right

    tree.value += value


def add_right(tree: Node, value: int) -> None:
    while tree.parent is not None:
        if tree.parent.left == tree:
            break
        tree = tree.parent

    tree = tree.parent

    if tree is None:
        return

    tree = tree.right

    while tree.value is None:
        tree = tree.left

    tree.value += value


def reduce_explode_rec(tree: Node, depth: int):
    if tree.left is None and tree.right is None:
        return tree, False

    if (depth >= 4 and tree.left.value is not None and
            tree.right.value is not None):
        add_left(tree, tree.left.value)
        add_right(tree, tree.right.value)
        return Node(value=0, parent=tree.parent), True

    left, status = reduce_explode_rec(tree.left, depth + 1)
    if status:
        tree.left = left
        left.parent = tree
        return tree, True

    right, status = reduce_explode_rec(tree.right, depth + 1)
    tree.right = right
    right.parent = tree
    return tree, status


def reduce_split_rec(tree: Node):
    if tree.left is None and tree.right is None:
        if tree.value < 10:
            return tree, False
        else:
            n1 = Node(value=(tree.value // 2))
            n2 = Node(value=tree.value - (tree.value // 2))
            n = Node(left=n1, right=n2)
            n1.parent = n
            n2.parent = n
            return n, True

    left, status = reduce_split_rec(tree.left)
    if status:
        tree.left = left
        left.parent = tree
        return tree, True

    right, status = reduce_split_rec(tree.right)
    tree.right = right
    right.parent = tree
    return tree, status


def reduce_operation(tree: Node) -> Node:
    while True:
        tree, flag = reduce_explode_rec(tree, 0)
        if flag:
            continue
        tree, flag = reduce_split_rec(tree)
        if not flag:
            return tree


def sum_operation(data: List[str]) -> Node:
    v1 = parse_tree(data[0])

    for i in range(1, len(data)):
        v2 = parse_tree(data[i])
        n = Node(left=v1, right=v2)
        v1.parent = n
        v2.parent = n
        v1 = reduce_operation(n)

    return v1


def magnitude(data: Node) -> int:
    if data.value is not None:
        return data.value
    return 3 * magnitude(data.left) + 2 * magnitude(data.right)


def largest_magnitude(data: List[str]) -> int:
    result = 0

    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                continue
            v1 = parse_tree(data[i])
            v2 = parse_tree(data[j])
            tree = Node(left=v1, right=v2)
            v1.parent = tree
            v2.parent = tree
            tree = reduce_operation(tree)

            result = max(result, magnitude(tree))

    return result


class TestClass():

    def test_1(self):
        data = parse_tree('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
        answer = '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
        assert str(reduce_operation(data)) == answer

    def test_2(self):
        data = [
            '[1,1]',
            '[2,2]',
            '[3,3]',
            '[4,4]',
        ]
        answer = '[[[[1,1],[2,2]],[3,3]],[4,4]]'
        assert str(sum_operation(data)) == answer

    def test_3(self):
        data = [
            '[1,1]',
            '[2,2]',
            '[3,3]',
            '[4,4]',
            '[5,5]',
        ]
        answer = '[[[[3,0],[5,3]],[4,4]],[5,5]]'
        assert str(sum_operation(data)) == answer

    def test_4(self):
        data = [
            '[1,1]',
            '[2,2]',
            '[3,3]',
            '[4,4]',
            '[5,5]',
            '[6,6]',
        ]
        answer = '[[[[5,0],[7,4]],[5,5]],[6,6]]'
        assert str(sum_operation(data)) == answer

    def test_5(self):
        data = [
            '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
            '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
            '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
            '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
            '[7,[5,[[3,8],[1,4]]]]',
            '[[2,[2,2]],[8,[8,1]]]',
            '[2,9]',
            '[1,[[[9,3],9],[[9,0],[0,7]]]]',
            '[[[5,[7,4]],7],1]',
            '[[[[4,2],2],6],[8,7]]',
        ]
        answer = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
        assert str(sum_operation(data)) == answer

    def test_6(self):
        data = [
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
            '[[[5,[2,8]],4],[5,[[9,9],0]]]',
            '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
            '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
            '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
            '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
            '[[[[5,4],[7,7]],8],[[8,3],8]]',
            '[[9,3],[[9,9],[6,[4,9]]]]',
            '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
            '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
        ]
        answer = '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'
        assert str(sum_operation(data)) == answer

    def test_7(self):
        data = parse_tree('[[1,2],[[3,4],5]]')
        assert magnitude(data) == 143

        data = parse_tree('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
        assert magnitude(data) == 1384

        data = parse_tree('[[[[1,1],[2,2]],[3,3]],[4,4]]')
        assert magnitude(data) == 445

        data = parse_tree('[[[[3,0],[5,3]],[4,4]],[5,5]]')
        assert magnitude(data) == 791

        data = parse_tree('[[[[5,0],[7,4]],[5,5]],[6,6]]')
        assert magnitude(data) == 1137

        data = parse_tree('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')
        assert magnitude(data) == 3488

        data = parse_tree('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
        assert magnitude(data) == 4140

    def test_8(self):
        data = [
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]',
            '[[[5,[2,8]],4],[5,[[9,9],0]]]',
            '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]',
            '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]',
            '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]',
            '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]',
            '[[[[5,4],[7,7]],8],[[8,3],8]]',
            '[[9,3],[[9,9],[6,[4,9]]]]',
            '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]',
            '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]',
        ]
        assert largest_magnitude(data) == 3993


def main():
    data = [x.strip() for x in sys.stdin]
    result = largest_magnitude(data)
    print(result)


if __name__ == '__main__':
    main()

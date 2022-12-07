#!/usr/bin/env python3

import sys
from typing import List, Dict


class Node:

    def __init__(
        self, name: str, back: 'Node' = None, is_dir: bool = True,
        size: int = -1
    ):
        self.name = name
        self.back = back
        self.is_dir = is_dir
        self.size = size
        self.children: Dict[str, 'Node'] = {}

    def print_tree(self, indent: int = 0):
        if self.is_dir:
            print(" " * indent, f"- {self.name} (dir, size={self.size})")
        else:
            print(" " * indent, f"- {self.name} (file, size={self.size})")

        for children in self.children.values():
            children.print_tree(indent=indent + 3)


def build_tree(data: List[str]) -> Node:
    tree = Node("/")
    curr_node = tree

    for line in data:
        if not line.startswith("$"):
            if line.startswith("dir"):
                name = line.rstrip().split()[-1]
                if name not in curr_node.children:
                    new_node = Node(name, back=curr_node)
                    curr_node.children[name] = new_node
            else:
                size, name = line.rstrip().split()
                if name not in curr_node.children:
                    new_node = Node(name, is_dir=False, size=int(size))
                    curr_node.children[name] = new_node
        elif line.startswith("$ cd"):
            path = line.rstrip().split()[-1]
            if path == "/":
                curr_node = tree
            elif path == "..":
                curr_node = curr_node.back if curr_node.back else tree
            elif path not in curr_node.children:
                new_node = Node(path, back=curr_node)
                curr_node.children[path] = new_node
                curr_node = new_node
            else:
                curr_node = curr_node.children[path]

    return tree


def calc_sizes(tree: Node) -> Node:

    stack = [tree]

    while stack:
        curr_node = stack.pop()
        if curr_node.is_dir:
            unknown_sizes = [
                item for item in curr_node.children.values() if item.size == -1
            ]
            if len(unknown_sizes):
                stack.append(curr_node)
                stack.extend(unknown_sizes)
            else:
                curr_node.size = sum(
                    item.size for item in curr_node.children.values()
                )

    return tree


def folders_score(data: List[str], top_limit: int = 100000) -> int:
    tree = calc_sizes(build_tree(data))

    result = 0
    stack = [tree]

    while stack:
        curr_node = stack.pop()
        if curr_node.is_dir:
            result += sum(
                item.size for item in curr_node.children.values()
                if item.is_dir and item.size <= top_limit
            )
            stack.extend(curr_node.children.values())

    tree.print_tree()

    return result


def test_folders_score():
    data = [
        '$ cd /',
        '$ ls',
        'dir a',
        '14848514 b.txt',
        '8504156 c.dat',
        'dir d',
        '$ cd a',
        '$ ls',
        'dir e',
        '29116 f',
        '2557 g',
        '62596 h.lst',
        '$ cd e',
        '$ ls',
        '584 i',
        '$ cd ..',
        '$ cd ..',
        '$ cd d',
        '$ ls',
        '4060174 j',
        '8033020 d.log',
        '5626152 d.ext',
        '7214296 k'
    ]

    assert folders_score(data) == 95437


def main():
    data = sys.stdin.readlines()
    result = folders_score(data)
    print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
from typing import Iterable, Dict, Tuple, Set, Optional


def parse_data(data: Iterable[str]) -> Dict[str, Set[str]]:
    graph = {}

    for line in data:
        v_head, v_tail = line.split(': ')
        v_tail = set(v_tail.split())

        if v_head not in graph:
            graph[v_head] = v_tail
        else:
            graph[v_head] = graph[v_head].union(v_tail)

        for v in v_tail:
            if v not in graph:
                graph[v] = {v_head}
            else:
                graph[v].add(v_head)

    return graph


def build_tree(graph: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    tree = {}

    root = list(graph.keys())[0]
    stack = [(root, None)]
    visited = set()

    while stack:
        v, v_prev = stack.pop()

        if v in visited:
            continue

        visited.add(v)

        if v_prev:
            if v not in tree:
                tree[v] = set()

            if v_prev not in tree:
                tree[v_prev] = set()

            tree[v].add(v_prev)
            tree[v_prev].add(v)

        for v_next in graph.get(v, set()):
            if v_next not in visited:
                stack.append((v_next, v))

    return tree


def find_first_part(
    tree: Dict[str, Set[str]], excludes: Set[Tuple[str, str]]
) -> Set[str]:

    root = list(tree.keys())[0]
    stack = [root]
    visited = set()

    while stack:
        v = stack.pop()
        visited.add(v)
        for v_next in tree.get(v, set()):
            if (min(v, v_next), max(v, v_next)) in excludes:
                continue
            if v_next not in visited:
                stack.append(v_next)

    return visited


def add_edge(graph: Dict[str, Set[str]], edge: Tuple[str, str]):
    v1, v2 = edge
    graph[v1].add(v2)
    graph[v2].add(v1)


def remove_edge(graph: Dict[str, Set[str]], edge: Tuple[str, str]):
    v1, v2 = edge
    graph[v1].remove(v2)
    graph[v2].remove(v1)


def find_bridge(graph: Dict[str, Set[str]]) -> Optional[Tuple[str, str]]:
    root = list(graph.keys())[0]
    stack = [(root, 0, None)]
    time_in, ret = {}, {}
    time = 0

    while stack:
        v, state, v_prev = stack.pop()

        if state == 1:
            if v_prev is not None:
                ret[v_prev] = min(ret[v_prev], ret[v])
                if ret[v] > time_in[v_prev]:
                    return (min(v, v_prev), max(v, v_prev))
            continue

        if v in time_in:
            continue

        time_in[v] = time
        ret[v] = time
        time += 1

        stack.append((v, 1, v_prev))

        for v_next in graph.get(v, set()):
            if v_next == v_prev:
                continue
            if v_next in time_in:
                ret[v] = min(ret[v], time_in[v_next])
            else:
                stack.append((v_next, 0, v))


def groups_score(data: Iterable[str]) -> int:
    graph = parse_data(data)
    tree = build_tree(graph)

    tree_edges = set(
        (min(v1, v2), max(v1, v2))
        for v1, v_set in tree.items()
        for v2 in v_set
    )

    tree_edges = list(tree_edges)
    used = set()

    for i in range(len(tree_edges)):
        print(f'{i}/{len(tree_edges)}', file=sys.stderr)

        remove_edge(graph, tree_edges[i])
        used.add(tree_edges[i])

        subtree = build_tree(graph)
        subtree_edges = set(
            (min(v1, v2), max(v1, v2))
            for v1, v_set in subtree.items()
            for v2 in v_set
        )

        for edge in subtree_edges:
            if edge in used:
                continue
            if edge[0] in tree_edges[i]:
                continue
            if edge[1] in tree_edges[i]:
                continue

            remove_edge(graph, edge)
            bridge = find_bridge(graph)
            add_edge(graph, edge)

            if not bridge:
                continue

            bridges = {bridge, edge, tree_edges[i]}
            print('found bridges', bridges, file=sys.stderr)

            part = find_first_part(graph, excludes=bridges)
            return len(part) * (len(graph) - len(part))

        add_edge(graph, tree_edges[i])

    return -1


def test_groups_score():
    data = [
        'jqt: rhn xhk nvd',
        'rsh: frs pzl lsr',
        'xhk: hfx',
        'cmg: qnr nvd lhk bvb',
        'rhn: xhk bvb hfx',
        'bvb: xhk hfx',
        'pzl: lsr hfx nvd',
        'qnr: nvd',
        'ntq: jqt hfx bvb xhk',
        'nvd: lhk',
        'lsr: lhk',
        'rzs: qnr cmg lsr rsh',
        'frs: qnr lhk lsr',
    ]
    assert groups_score(data) == 54


def main():
    data = (line.rstrip() for line in sys.stdin)
    data = (line for line in data if len(line))
    result = groups_score(data)
    print(result)


if __name__ == '__main__':
    main()

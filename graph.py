#!/usr/bin/env python3

from random import randint, shuffle
from collections import defaultdict


class DisjointSet(object):
    ''' DisjointSet(number_of_elements) -> instance of DisjointSet

    >>> DisjointSet(5)
    DisjointSet([{0}, {1}, {2}, {3}, {4}])
    >>> ds = DisjointSet([{0}, {1, 3}, {2, 4}])
    >>> ds
    DisjointSet([{0}, {1, 3}, {2, 4}])
    >>> ds.union(0, 1)
    >>> ds
    DisjointSet([{2, 4}, {0, 1, 3}])
    >>> ds.group_count
    2

    Simple data structure for checking if graph is connected?
    '''

    def union(self, u, v):
        if self.find(u) != self.find(v):
            self.group_count -= 1
        self.parent[self.find(u)] = self.find(v)

    def find(self, u):
        if self.parent[u] == u:
            return u
        self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def __repr__(self):
        groups = defaultdict(set)
        for u in self.parent:
            groups[self.find(u)] |= {u}
        return 'DisjointSet({})'.format(sorted(groups.values(), key=len))

    def __init__(self, groups):
        if isinstance(groups, int):
            self.parent = {i: i for i in range(groups)}
            self.group_count = groups
        else:
            self.parent = {i: i for group in groups for i in group}
            self.group_count = max(max(group) for group in groups) + 1
            for group in groups:
                u = group.pop()
                for v in group:
                    self.union(u, v)


class RandomConnectedGraph(object):
    ''' RandomConnectedGraph(number_of_nodes) -> instance of RandomConnectedGraph

    >>> graph = RandomConnectedGraph(2)
    >>> graph
    RandomConnectedGraph({(0, 1)})
    >>> graph.connected()
    True

    RandomConnectedGraph which test connectivity using union-find technique.
    '''

    def add(self, i, j):
        self.graph |= {(i, j)}
        self._disjoint_set.union(i, j)

    def random_add(self):
        i, j = self._random_queue.pop()
        self.add(i, j)

    def connected(self):
        return self._disjoint_set.group_count == 1

    def _make_random_queue(self):
        self._random_queue = []
        for i in range(self.nodes):
            for j in range(i+1, self.nodes):
                self._random_queue += [(i, j)]
        shuffle(self._random_queue)

    def __iter__(self):
        return iter(self.graph)

    def __repr__(self):
        return 'RandomConnectedGraph({})'.format(self.graph)

    def __init__(self, nodes):
        if isinstance(nodes, int):
            self.graph = set()
            self.nodes = nodes
            self._disjoint_set = DisjointSet(self.nodes)
        else:
            self.graph = nodes
            self.nodes = max(max(node) for node in nodes) + 1
            self._disjoint_set = DisjointSet(self.nodes)
            for i, j in nodes:
                self.add(i, j)
        self._make_random_queue()
        while not self.connected():
            self.random_add()

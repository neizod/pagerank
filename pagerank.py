#!/usr/bin/env python3

import sys
from random import random


class GraphToMatrix(object):
    ''' GraphToMatrix(graph) -> instance of GraphToMatrix

    >>> gm = GraphToMatrix([(0,1), (1,2), (2,3), (0,2)])
    >>> for row in gm.adjacency(): print(row)
    [0, 1, 1, 0]
    [1, 0, 1, 0]
    [1, 1, 0, 1]
    [0, 0, 1, 0]
    >>> gm.degree()
    [2, 2, 3, 1]
    >>> gm.nodes()
    4

    Helper class that try to representation graph with matrix.
    '''

    def adjacency(self):
        A = [[0 for _ in range(self.nodes())] for _ in range(self.nodes())]
        for i, j in self.graph:
            A[i][j] = 1
            if not self.directed:
                A[j][i] = 1
        return A

    def degree(self):
        D = [0 for _ in range(self.nodes())]
        for i, j in self.graph:
            D[i] += 1
            if not self.directed:
                D[j] += 1
        return D

    def nodes(self):
        return max(i for pair in self.graph for i in pair) + 1

    def __init__(self, graph, directed=False):
        self.graph = graph
        self.directed = directed


class PageRank(object):
    ''' PageRank(graph, alpha, epsilon) -> instance of PageRank

    >>> pr = PageRank([(0,1), (1,2), (2,3), (0,2)], alpha=0.1, epsilon=0.001)
    >>> pr.pagerank
    [0, 0, 0, 0]
    >>> pr.push(0); pr.pagerank
    [0.025, 0, 0, 0]
    >>> pr.push(0); pr.pagerank    # doctest: +ELLIPSIS
    [0.03625..., 0, 0, 0]
    >>> pr.calculate()             # doctest: +ELLIPSIS
    [0.24363..., 0.24373..., 0.36232..., 0.14416...]

    PageRank object for calculating approximate epsilon-PageRank.
    '''

    def calculate(self):
        while True:
            for u in range(self.nodes):
                if self.residue[u] >= self.epsilon * self.degree[u]:
                    if self.push(u):
                        break
            else:
                break
        return self.pagerank

    def neighborhood(self, u):
        yield from (v for v, s in enumerate(self.adjacency[u]) if s == 1)

    def push(self, u):
        taken = self.alpha * self.residue[u]
        remains = self.residue[u] - taken
        self.pagerank[u] += taken
        self.residue[u] = remains / 2
        if self.degree[u] == 0:
            return False
        for v in self.neighborhood(u):
            self.residue[v] += (remains / 2) / self.degree[u]
        return True

    def __init__(self, graph, alpha=0.05, epsilon=0.0001, directed=False):
        self.alpha = alpha
        self.epsilon = epsilon

        graph_as_matrix = GraphToMatrix(graph, directed)
        self.adjacency = graph_as_matrix.adjacency()
        self.degree = graph_as_matrix.degree()
        self.nodes = graph_as_matrix.nodes()

        self.pagerank = [0 for _ in range(self.nodes)]
        self.residue = [1/self.nodes for _ in range(self.nodes)]


def read_graph_and_options(file):
    defaults = {}
    while True:
        line = file.readline().strip()
        if line == '---':
            break
        parameter, value = line.split()
        parameter = parameter.lower()
        if parameter in ['alpha', 'epsilon']:
            defaults[parameter] = float(value)
        if parameter in ['directed']:
            defaults[parameter] = value.lower() in ['t', 'y', 'true', 'yes']
    graph = [tuple(int(n) for n in line.split()) for line in file.readlines()]
    return graph, defaults


def main():
    if len(sys.argv) != 2:
        exit('usage: {} GRAPHFILE'.format(__file__))
    graphfile = sys.argv[1]

    graph, defaults = read_graph_and_options(open(graphfile))
    pagerank = PageRank(graph, **defaults).calculate()
    print(['{:.5f}'.format(i) for i in pagerank])

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import sys
from graph import DisjointSet, RandomConnectedGraph

def main():
    if len(sys.argv) != 2:
        exit('usage: {} NODES'.format(__file__))
    nodes = int(sys.argv[1])

    G = RandomConnectedGraph(nodes)
    for a, b in G:
        print(a, b)

if __name__ == '__main__':
    main()

import sys
from collections import deque


graph = {}



def bfs():
    q = deque()
    parents = {'a': None}
    reachable = []
    visited = set()
    q.append(('a', 0))
    visited.add('a')
    while len(q) > 0:
        current, dist = q.popleft()
        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                if neighbour.isupper():
                    reachable.append((dist + 1, neighbour))
                parents[neighbour] = current
                q.append((neighbour, dist + 1))
    return sorted(reachable), parents


def solve() -> list[str]:
    result = []
    while True:
        reachable, parents = bfs()

        if len(reachable) == 0:
            return result

        _, node = reachable[0]
        parent = parents[node]

        result.append(f"{node}-{parent}")
        graph[parent].remove(node)


def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                if node1.isupper():
                    node1, node2 = node2, node1
                if node1 not in graph:
                    graph[node1] = []
                graph[node1].append(node2)

    result = solve()
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()

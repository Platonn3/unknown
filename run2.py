import sys
from collections import deque
import copy


graph = {}

def bfs(current_node: str, labyrinth: dict[str, str]) -> tuple[list[tuple[int, str]], dict[str, str|None]]:
    q = deque()
    parents = {current_node: None}
    reachable = []
    visited = set()
    q.append((current_node, 0))
    visited.add(current_node)
    while len(q) > 0:
        current, dist = q.popleft()
        for neighbour in sorted(labyrinth.get(current, [])):
            if neighbour not in visited:
                visited.add(neighbour)
                if neighbour.isupper():
                    reachable.append((dist + 1, neighbour))
                parents[neighbour] = current
                q.append((neighbour, dist + 1))
    return reachable, parents


def can_virus_reach_gateway(copied_graph: dict[str, str], virus_pos: str) -> bool:
    reachable, _ = bfs(virus_pos, copied_graph)
    if len(reachable) == 0:
        return False
    reachable.sort()
    return reachable[0][0] == 1


def find_next_position(parents: dict[str, str|None], final_node: str) -> str|None:
    result = final_node
    while parents[final_node] is not None:
        result = final_node
        final_node = parents[final_node]
    return result


def solve() -> list[str]:
    current_position = 'a'
    result = []

    while True:
        reachable, parents = bfs(current_position, graph)

        if len(reachable) == 0:
            return result

        reachable.sort(key=lambda x: x[1])

        gateway = ""
        node = ""
        for _, gateway in reachable:
            node = parents[gateway]
            copied_graph = copy.deepcopy(graph)
            copied_graph[gateway].remove(node)
            copied_graph[node].remove(gateway)
            if not can_virus_reach_gateway(copied_graph, current_position):
                break

        result.append(f"{gateway}-{node}")
        graph[gateway].remove(node)
        graph[node].remove(gateway)

        reachable, parents = bfs(current_position, graph)
        if len(reachable) == 0:
            return result

        reachable.sort()
        _, gateway = reachable[0]
        current_position = find_next_position(parents, gateway)


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                if node1 not in graph:
                    graph[node1] = set()
                if node2 not in graph:
                    graph[node2] = set()
                graph[node1].add(node2)
                graph[node2].add(node1)
    result = solve()
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()

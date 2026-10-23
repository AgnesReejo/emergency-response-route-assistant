"""Graph-search algorithms for the simulated emergency road network."""
from collections import deque
import heapq
import math


def build_graph(problem):
    graph = {node["name"]: [] for node in problem["nodes"]}
    for road in problem["roads"]:
        if road.get("blocked", False):
            continue
        a, b = road["from"], road["to"]
        # Roads are treated as two-way in this teaching prototype.
        graph[a].append((b, road))
        graph[b].append((a, road))
    return graph


def route_metrics(path, problem):
    total_time = 0
    total_distance = 0.0
    roads = []
    for a, b in zip(path, path[1:]):
        road = next((r for r in problem["roads"] if not r.get("blocked", False) and
                     {r["from"], r["to"]} == {a, b}), None)
        if road is None:
            raise ValueError(f"No open road connects {a} and {b}")
        total_time += float(road["time"])
        total_distance += float(road["distance"])
        roads.append(road)
    return {"path": path, "travel_time": total_time, "distance": round(total_distance, 2), "roads": roads}


def bfs(problem, start, goal):
    graph = build_graph(problem)
    if start not in graph or goal not in graph:
        return None, 0
    queue = deque([(start, [start])])
    seen = {start}
    expanded = 0
    while queue:
        node, path = queue.popleft()
        expanded += 1
        if node == goal:
            return route_metrics(path, problem), expanded
        for nxt, _ in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None, expanded


def _weighted_search(problem, start, goal, use_heuristic=False):
    graph = build_graph(problem)
    coords = {n["name"]: (float(n.get("x", 0)), float(n.get("y", 0))) for n in problem["nodes"]}
    if start not in graph or goal not in graph:
        return None, 0
    def heuristic(node):
        # Admissible for this sample: travel time is at least 1.5 minutes per coordinate unit.
        x1, y1 = coords[node]; x2, y2 = coords[goal]
        return math.hypot(x2-x1, y2-y1) * 1.0 if use_heuristic else 0.0
    heap = [(heuristic(start), 0.0, start, [start])]
    best = {start: 0.0}
    expanded = 0
    while heap:
        _, cost, node, path = heapq.heappop(heap)
        if cost > best.get(node, float("inf")):
            continue
        expanded += 1
        if node == goal:
            return route_metrics(path, problem), expanded
        for nxt, road in graph[node]:
            new_cost = cost + float(road["time"])
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(heap, (new_cost + heuristic(nxt), new_cost, nxt, path + [nxt]))
    return None, expanded


def ucs(problem, start, goal):
    """Find minimum-travel-time route using Uniform-Cost Search."""
    return _weighted_search(problem, start, goal, False)


def astar(problem, start, goal):
    """A* using a straight-line coordinate heuristic in simulated map units."""
    return _weighted_search(problem, start, goal, True)

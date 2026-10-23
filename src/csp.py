"""A small constraint-based route enumerator for demonstration (not an optimizer)."""
from .search import build_graph, route_metrics


def find_feasible_routes(problem, start, goal, max_routes=10, max_depth=None):
    graph = build_graph(problem)
    if start not in graph or goal not in graph:
        return []
    max_depth = max_depth or len(graph)
    routes = []
    def backtrack(current, path):
        if len(routes) >= max_routes:
            return
        if current == goal:
            routes.append(route_metrics(path, problem))
            return
        if len(path) >= max_depth:
            return
        for nxt, _ in graph[current]:
            # Constraint: no repeated node; only open roads appear in graph.
            if nxt not in path:
                backtrack(nxt, path + [nxt])
    backtrack(start, [start])
    return sorted(routes, key=lambda r: (r["travel_time"], r["distance"]))

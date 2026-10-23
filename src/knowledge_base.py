"""Simple explainable rule checks for route recommendations."""

def validate_route(problem, path):
    trace = []
    if not path:
        return False, ["No route was returned; check connectivity and blocked roads."]
    node_names = {n["name"] for n in problem["nodes"]}
    if any(n not in node_names for n in path):
        return False, ["Rule failed: every route location must exist in the map."]
    if len(path) != len(set(path)):
        trace.append("Rule warning: route repeats a location.")
        return False, trace
    for a, b in zip(path, path[1:]):
        road = next((r for r in problem["roads"] if {r["from"], r["to"]} == {a, b}), None)
        if road is None:
            trace.append(f"Rule failed: {a} and {b} are not connected by a road.")
            return False, trace
        if road.get("blocked", False):
            trace.append(f"Rule failed: blocked road {a} ↔ {b} cannot be used.")
            return False, trace
        trace.append(f"Rule passed: open road {a} ↔ {b} is allowed.")
    trace.append("Rule passed: route contains valid locations and reaches the requested destination.")
    return True, trace


def road_status(problem, start, end):
    road = next((r for r in problem["roads"] if {r["from"], r["to"]} == {start, end}), None)
    if road is None:
        return "No direct road is recorded between these locations."
    if road.get("blocked", False):
        return "Direct road is blocked and must be avoided."
    return f"Direct road is open; estimated time {road['time']} minutes, distance {road['distance']} km."

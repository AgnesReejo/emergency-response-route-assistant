"""Agent description and input validation."""

def describe_agent():
    return {
        "agent_type": "Goal-based route-planning agent",
        "performance": "Minimize simulated travel time; avoid blocked roads; reach destination.",
        "environment": "A simulated city graph with locations and road conditions.",
        "actuators": "Display route, travel time, distance, and explored-node count.",
        "sensors": "Origin/destination selections, road travel times, distances, and block status.",
    }


def validate_problem(problem):
    errors = []
    names = [n.get("name") for n in problem.get("nodes", [])]
    if not names or any(not n for n in names):
        errors.append("Each map node must have a name.")
    if len(names) != len(set(names)):
        errors.append("Node names must be unique.")
    name_set = set(names)
    for i, road in enumerate(problem.get("roads", []), start=1):
        if road.get("from") not in name_set or road.get("to") not in name_set:
            errors.append(f"Road {i} refers to a location that is not in the node list.")
        if float(road.get("time", 0)) <= 0:
            errors.append(f"Road {i} must have a positive travel time.")
        if float(road.get("distance", 0)) <= 0:
            errors.append(f"Road {i} must have a positive distance.")
    return errors

"""Command-line demo: python -m src.main"""
import json
from pathlib import Path
from .agent import describe_agent, validate_problem
from .search import bfs, ucs, astar
from .knowledge_base import validate_route

ROOT = Path(__file__).resolve().parents[1]

def main():
    problem = json.loads((ROOT / "data" / "sample_city.json").read_text(encoding="utf-8"))
    errors = validate_problem(problem)
    if errors:
        print("Input errors:", *errors, sep="\n- "); return
    print("EMERGENCY RESPONSE ROUTE ASSISTANT (SIMULATION)")
    print("PEAS:", json.dumps(describe_agent(), indent=2))
    names = [n["name"] for n in problem["nodes"]]
    print("Locations:", ", ".join(names))
    start = input("Start location [Central Station]: ").strip() or "Central Station"
    goal = input("Destination [City Hospital]: ").strip() or "City Hospital"
    for label, fn in [("BFS", bfs), ("UCS", ucs), ("A*", astar)]:
        result, expanded = fn(problem, start, goal)
        print(f"\n{label}: explored={expanded}")
        if result:
            print("Route:", " -> ".join(result["path"]))
            print(f"Travel time: {result['travel_time']} minutes; distance: {result['distance']} km")
            print("Logic validation:", validate_route(problem, result["path"])[0])
        else:
            print("No valid route found.")

if __name__ == "__main__":
    main()

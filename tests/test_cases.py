import json
import unittest
from pathlib import Path
from src.search import bfs, ucs, astar
from src.knowledge_base import validate_route
from src.agent import validate_problem

ROOT = Path(__file__).resolve().parents[1]

def load_problem():
    return json.loads((ROOT / "data" / "sample_city.json").read_text(encoding="utf-8"))

class RouteAssistantTests(unittest.TestCase):
    def test_sample_input_valid(self):
        self.assertEqual(validate_problem(load_problem()), [])

    def test_ucs_and_astar_find_route(self):
        p = load_problem()
        u, _ = ucs(p, "Central Station", "City Hospital")
        a, _ = astar(p, "Central Station", "City Hospital")
        self.assertIsNotNone(u)
        self.assertIsNotNone(a)
        self.assertEqual(u["travel_time"], a["travel_time"])

    def test_blocked_road_avoided(self):
        p = load_problem()
        for road in p["roads"]:
            if {road["from"], road["to"]} == {"River Bridge", "City Hospital"}:
                road["blocked"] = True
        route, _ = ucs(p, "Central Station", "City Hospital")
        self.assertIsNotNone(route)
        self.assertNotIn(["River Bridge", "City Hospital"], [route["path"][i:i+2] for i in range(len(route["path"])-1)])

    def test_no_route_when_all_connections_blocked(self):
        p = load_problem()
        for road in p["roads"]:
            road["blocked"] = True
        route, _ = ucs(p, "Central Station", "City Hospital")
        self.assertIsNone(route)

    def test_logic_validation(self):
        p = load_problem()
        ok, trace = validate_route(p, ["Central Station", "Market Junction", "River Bridge"])
        self.assertTrue(ok)
        self.assertTrue(trace)

    def test_same_origin_and_destination(self):
        route, _ = ucs(load_problem(), "Central Station", "Central Station")
        self.assertEqual(route["path"], ["Central Station"])
        self.assertEqual(route["travel_time"], 0)

if __name__ == "__main__":
    unittest.main()

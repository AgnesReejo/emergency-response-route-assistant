# Proposed Methodology

## 1. Title
**Emergency Response Route Assistant using AI Search (SDG 3 and SDG 11)**

## 2. Problem statement
Emergency vehicles need routes that avoid unavailable roads and reach a destination efficiently. The project models a small city as a graph and demonstrates how AI search algorithms can find routes under simulated road conditions. It does not use live maps, traffic, or dispatch services.

## 3. Objectives
1. Represent a city road network as a graph.
2. Design a goal-based intelligent agent using the PEAS framework.
3. Compare BFS, Uniform-Cost Search, and A* Search.
4. Apply constraint checks to exclude blocked roads and repeated locations.
5. Create a small knowledge base that explains route validity.
6. Provide a frontend for changing road conditions and inspecting results.
7. Test the implementation using both valid and failure scenarios.

## 4. System inputs and outputs
**Inputs:** named locations, road endpoints, estimated travel time, distance, blocked/open status, origin, and destination.

**Outputs:** a recommended path, estimated travel time, total distance, nodes explored, feasible alternative routes, and rule-validation messages.

## 5. Intelligent-agent description (CO1)
The system is a goal-based route-planning agent.
- **Performance measure:** reach the goal, minimize estimated travel time, avoid blocked roads, and provide a clear explanation.
- **Environment:** a simulated city represented as a graph.
- **Actuators:** display route and metrics in the user interface or terminal.
- **Sensors:** user selections and road-condition data.

## 6. Graph model and search methods (CO2)
Each location is a node. Each road is an undirected edge with a travel-time cost and distance. Blocked edges are omitted from the searchable graph.
- **BFS:** finds a path with the fewest edges when all edges are treated equally.
- **UCS:** expands the lowest accumulated travel-time cost first and returns a minimum-time route for non-negative edge costs.
- **A*:** ranks candidates by accumulated travel time plus a heuristic estimate to the destination. The sample uses Euclidean coordinate distance multiplied by 1.0 as a lower-bound heuristic for its example edges; UCS is the safe optimal baseline if a valid lower-bound heuristic cannot be guaranteed for a modified map.

## 7. Constraint satisfaction and backtracking (CO3)
The CSP demonstration treats a candidate route as a sequence of locations. Constraints are: the start must be the first location; the goal must be reached; every consecutive pair must have an edge; blocked edges are forbidden; and locations cannot repeat. Backtracking builds candidate paths while checking constraints. The demo enumerates a bounded number of feasible simple routes and ranks those returned by travel time and distance. UCS/A* perform the primary optimization.

## 8. Knowledge representation and inference (CO4)
The knowledge base implements explicit rules:
1. A route location must exist in the map.
2. Consecutive route locations must be connected by a recorded road.
3. A blocked road cannot be traversed.
4. A simple route should not repeat locations.
5. If no route is found, the system must report failure rather than fabricate a path.

The application presents rule-check messages so users can inspect why a route passed validation or why a direct road is unavailable.

## 9. Frontend workflow
1. Load the sample road network.
2. Edit locations and roads if desired.
3. Set road travel time, distance, and blocked status.
4. Choose origin and destination.
5. Run one or all search algorithms.
6. Compare paths, estimated times, distances, and explored nodes.
7. Inspect feasible alternatives and logic trace.

## 10. Testing and evaluation
Unit tests cover valid input, route existence, agreement between UCS and A* on the sample, avoidance of a blocked road, disconnected-network failure, logic validation, and identical origin/destination. Evaluation measures include route travel time, distance, nodes explored, and successful handling of blocked-road scenarios.

## 11. SDG connection
- **SDG 3:** illustrates how route planning can support access to hospitals and emergency destinations.
- **SDG 11:** demonstrates urban route resilience when roads are unavailable.

These are educational connections only; the prototype does not establish real-world reductions in response times or health outcomes.

## 12. Limitations and future work
The data is simulated; roads are two-way; no live GPS, traffic, weather, road closure feeds, emergency dispatch, or road safety rules are integrated. Future versions could use validated public map data, directional roads, time-dependent travel estimates, accessibility restrictions, and formal safety review. Any real-world deployment would require reliable data, testing, and emergency-service oversight.

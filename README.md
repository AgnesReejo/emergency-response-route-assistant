# Group 2 Members

Adhithya Subash (CCE23CS007) 
Adith V A (CCE23CS008) 
Adithyan C P (CCE23CS009) 
Agatha Varghese (CCE23CS010) 
Agnel Chackochan (CCE23CS011) 
Agnes Reejo Parayil (CCE23CS012)

# Emergency Response Route Assistant (SDG 3 & SDG 11)

A small educational AI prototype that finds routes through a simulated city road network. It demonstrates an intelligent agent, graph search, constraint checking, logic-based explanations, testing, and an interactive Streamlit frontend.

> **Safety note:** This project uses invented locations and simulated travel times. It is not connected to live traffic, maps, dispatch, or emergency services and must not be used for real emergency decisions.

## Features
- Editable locations and roads in the frontend.
- Toggle road blockages and compare BFS, Uniform-Cost Search (UCS), and A*.
- Show route, simulated travel time, distance, and number of explored nodes.
- Backtracking constraint solver to enumerate feasible simple routes.
- Rule-based route validation and direct-road status explanation.
- Unit tests for route availability, blocked roads, optimal-cost agreement, and input validation.

## Project structure
```text
emergency_response_route_assistant/
├── app.py
├── README.md
├── requirements.txt
├── AI_USE.md
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── search.py
│   ├── csp.py
│   ├── knowledge_base.py
│   └── main.py
├── data/sample_city.json
├── tests/test_cases.py
├── results/test_results.md
└── docs/proposed_methodology.md
```

## Run the frontend
Use Python 3.10 or newer.
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open the local URL printed by Streamlit in your browser. Edit the locations and roads in the sidebar, mark roads blocked, choose an origin and destination, then select **Find emergency route**.

## Run the command-line version
```bash
python -m src.main
```
Use exact location names from the sample map, or press Enter to accept the defaults.

## Run tests
From the project root:
```bash
python -m unittest discover -s tests -v
```

## AI concepts and course outcomes
- **CO1 — Intelligent agent:** PEAS description in `src/agent.py`.
- **CO2 — Search:** BFS, UCS, and A* in `src/search.py`.
- **CO3 — CSP/search:** Backtracking enumerator in `src/csp.py`, enforcing adjacency, open-road, and no-repeated-location constraints.
- **CO4 — Logic and inference:** Explainable rule checks in `src/knowledge_base.py`.

## Simplifying assumptions
- Every road is two-way.
- Travel time and distance are entered manually and are simulated.
- A blocked road is unavailable in both directions.
- A* uses Euclidean distance multiplied by 1.0 as an illustrative heuristic. For a different map, verify that the heuristic is a lower bound on remaining travel time; otherwise use UCS for guaranteed minimum-time results.
- BFS minimizes the number of road segments, not travel time.
- The CSP component demonstrates feasibility enumeration; UCS/A* are the route optimizers.

import json
from pathlib import Path
import pandas as pd
import streamlit as st
from src.agent import describe_agent, validate_problem
from src.search import bfs, ucs, astar
from src.csp import find_feasible_routes
from src.knowledge_base import validate_route, road_status

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Emergency Route Assistant", page_icon="🚑", layout="wide")
st.title("🚑 Emergency Response Route Assistant")
st.caption("AI search demonstration for SDG 3 and SDG 11 • Simulated roads only; not for real emergencies.")

@st.cache_data
def load_sample():
    return json.loads((ROOT / "data" / "sample_city.json").read_text(encoding="utf-8"))

sample = load_sample()
if "nodes_df" not in st.session_state:
    st.session_state.nodes_df = pd.DataFrame(sample["nodes"])
if "roads_df" not in st.session_state:
    st.session_state.roads_df = pd.DataFrame(sample["roads"])

with st.sidebar:
    st.header("1. Map input")
    st.write("Edit the sample city or restore the default map.")
    if st.button("Restore sample map"):
        st.session_state.nodes_df = pd.DataFrame(sample["nodes"])
        st.session_state.roads_df = pd.DataFrame(sample["roads"])
    st.subheader("Locations")
    nodes_df = st.data_editor(st.session_state.nodes_df, num_rows="dynamic", use_container_width=True, key="nodes_editor")
    st.subheader("Roads")
    roads_df = st.data_editor(st.session_state.roads_df, num_rows="dynamic", use_container_width=True, key="roads_editor", column_config={"blocked": st.column_config.CheckboxColumn("Blocked?")})
    st.caption("Roads are treated as two-way. Travel time is in minutes and distance in km.")

problem = {"nodes": nodes_df.fillna(0).to_dict(orient="records"), "roads": roads_df.fillna(0).to_dict(orient="records")}
for r in problem["roads"]:
    r["blocked"] = bool(r.get("blocked", False))
    r["time"] = float(r.get("time", 0))
    r["distance"] = float(r.get("distance", 0))
errors = validate_problem(problem)
if errors:
    st.error("Please fix map input errors: " + " | ".join(errors))
    st.stop()

names = [n["name"] for n in problem["nodes"]]
left, right = st.columns(2)
with left:
    start = st.selectbox("2. Starting location", names, index=names.index("Central Station") if "Central Station" in names else 0)
with right:
    goal = st.selectbox("3. Destination", names, index=names.index("City Hospital") if "City Hospital" in names else min(1, len(names)-1))
algorithm = st.radio("4. Choose search algorithm", ["Compare all", "BFS", "Uniform-Cost Search (UCS)", "A* Search"], horizontal=True)

if st.button("Find emergency route", type="primary", use_container_width=True):
    methods = {"BFS": bfs, "Uniform-Cost Search (UCS)": ucs, "A* Search": astar}
    chosen = [("BFS", bfs), ("UCS", ucs), ("A*", astar)] if algorithm == "Compare all" else [(algorithm, methods[algorithm])]
    results = []
    for label, fn in chosen:
        route, expanded = fn(problem, start, goal)
        results.append((label, route, expanded))
    st.subheader("Recommended route results")
    cols = st.columns(len(results))
    for col, (label, route, expanded) in zip(cols, results):
        with col:
            st.markdown(f"#### {label}")
            st.metric("Nodes explored", expanded)
            if route:
                st.success(" → ".join(route["path"]))
                st.metric("Estimated travel time", f"{route['travel_time']:.0f} min")
                st.metric("Distance", f"{route['distance']:.1f} km")
                ok, trace = validate_route(problem, route["path"])
                st.write("Logic validation:", "PASS" if ok else "FAIL")
            else:
                st.warning("No valid route found.")
    st.subheader("Constraint solver (CO3 demonstration)")
    feasible = find_feasible_routes(problem, start, goal, max_routes=5)
    if feasible:
        st.dataframe(pd.DataFrame([{"Route": " → ".join(r["path"]), "Time (min)": r["travel_time"], "Distance (km)": r["distance"]} for r in feasible]), use_container_width=True)
        st.caption("Backtracking enumerates feasible simple routes and sorts the first routes found by cost; UCS/A* are the optimal search methods.")
    else:
        st.info("No feasible route exists under the current road constraints.")
    st.subheader("Logic / explainability trace")
    primary = next((r for _, r, _ in results if r), None)
    if primary:
        ok, trace = validate_route(problem, primary["path"])
        for item in trace:
            st.write(("✅ " if "passed" in item.lower() else "⚠️ ") + item)
    else:
        st.write("Rule: if no path exists through open roads, report no route rather than inventing one.")

st.divider()
st.subheader("Knowledge base: direct road status")
qa1, qa2 = st.columns(2)
with qa1:
    road_a = st.selectbox("From", names, key="qa_from")
with qa2:
    road_b = st.selectbox("To", names, index=min(1, len(names)-1), key="qa_to")
st.info(road_status(problem, road_a, road_b))
with st.expander("Intelligent agent description (PEAS)"):
    for key, value in describe_agent().items():
        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
st.warning("Educational simulation only. Do not use this application for live dispatch, navigation, or real emergency decisions. Call your local emergency number in a real emergency.")

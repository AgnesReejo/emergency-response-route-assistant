# Test Results

Run from the repository root with `python -m unittest discover -s tests -v` and update this report with the actual output before submission.

| Test | Expected result |
|---|---|
| Sample input validation | No input errors |
| UCS and A* route search | Both find a route with the same minimum travel-time cost on sample map |
| Blocked road | Route avoids the blocked road when an alternative exists |
| All roads blocked | No route is returned |
| Logic validation | Valid open-road path passes checks |
| Same start and goal | Single-location route with zero time and distance |

**Submission reminder:** paste or summarize the real test run here; do not represent expected results as actual results until tests have been executed.

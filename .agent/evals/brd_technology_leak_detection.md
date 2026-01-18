---
type: evaluation
name: "BRD Technology Leak Detection"
description: "Ensures BRD tags contain no technology-specific terms."
target_agent: "@brd_strategist"
threshold: 100
metrics:
  - name: clean_brd_rate
    type: percentage
    target: 100
test_cases: "needs.json"
schedule: "on_demand"
---

# Evaluation: BRD Technology Leak Detection

## Test Procedure

1. Load BRD tags from `docs/_build/json/needs.json`
2. Check each BRD for forbidden terms: Python, JavaScript, SQL, API, REST, GraphQL, HTTP, JSON, XML, database, server, client, endpoint, microservice, container, Docker, Kubernetes, AWS, Azure, GCP, framework, library
3. Calculate: `clean_rate = ((total - violations) / total) * 100`
4. Pass if `clean_rate == 100`

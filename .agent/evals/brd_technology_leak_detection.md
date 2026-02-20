---
type: evaluation
name: "BRD Technology Leak Detection"
target_agent: "@brd_strategist"
judge_model: "gemini-3.1-pro"
pass_threshold: 100
scenarios:
  - "Scan BRD tags for technology-specific keywords"
  - "Verify detected leaks in test set"
rubric:
  - "Zero technology terms in BRD tags"
  - "Must detect all seeded technology terms"
---

# Evaluation: BRD Technology Leak Detection

## Test Procedure

1. Load BRD tags from `docs/_build/json/needs.json`
2. Check each BRD for forbidden terms: Python, JavaScript, SQL, API, REST, GraphQL, HTTP, JSON, XML, database, server, client, endpoint, microservice, container, Docker, Kubernetes, AWS, Azure, GCP, framework, library
3. Calculate: `clean_rate = ((total - violations) / total) * 100`
4. Pass if `clean_rate == 100`

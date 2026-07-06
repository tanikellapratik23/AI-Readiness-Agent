# Prototype Architecture

This Phase 1 prototype is intentionally lightweight and modular. The design supports future expansion into role-adaptive agent behavior, a RAG knowledge base, and a dashboard.

## Components

- `app.py`
  - User-facing interface
  - Role selection and assessment orchestration
  - Simple chatbot interaction loop

- `framework.py`
  - Defines stakeholder roles
  - Defines readiness dimensions and assessment questions
  - Stores dimension-level recommendations

- `assessment.py`
  - Translates answers into numeric scores
  - Aggregates scores by dimension and overall readiness
  - Builds tailored recommendations based on role and score

## Data flow

User -> CLI (app.py) -> Assessment engine (`assessment.py`) -> Score generation -> Recommendations

## Readiness dimensions

- Governance & Policy
- Systems & Infrastructure
- Culture & Skills
- Education & Training

## Extension points

- Add a database or storage layer to persist assessment results
- Add a web UI or dashboard for visualizations
- Add a RAG knowledge base for informed answer generation
- Add role-specific question sets and tailored messaging

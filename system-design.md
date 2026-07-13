# System Design: Higher Education AI Readiness Agent

## 1. Purpose

The agent's goal is to help stakeholders in higher education (students, faculty, leadership, business affairs, communications) understand and improve their institution's readiness to adopt AI responsibly. The system takes stakeholders through a structured self-assessment, produces a readiness score across four dimensions, gives tailored recommendations, and lets them ask follow-up questions through a role-aware chatbot.

This document covers the as-built Phase 1 prototype and the target architecture for Phase 2 (role-adaptive agent) and Phase 3 (organizational platform), based on the current codebase (`app.py`, `agent.py`, `assessment.py`, `framework.py`, `app.js`).

---

## 2. Phase 1 — As-Built Architecture

Phase 1 is a monolithic, file-based prototype with **two parallel front ends that share one core scoring model but currently duplicate its logic**:

- A **Python CLI** (`app.py`) that drives `framework.py` + `assessment.py` + `agent.py` directly, no server involved.
- A **static web UI** (`app.js` + HTML/CSS, not yet uploaded) that reimplements the same questions, scoring, and rule-based chatbot logic in JavaScript, and optionally calls an external `window.CHAT_API_URL + '/chat'` endpoint if one is configured.

There is no persistence layer yet — everything lives in memory for the duration of a session.

### 2.1 Component responsibilities

| File | Responsibility |
|---|---|
| `framework.py` | Source of truth for stakeholder roles, the 8 assessment questions (mapped to 4 dimensions), and dimension-level recommendation text. *(Referenced by `app.py`/`assessment.py`, not in the uploaded set.)* |
| `assessment.py` | Pure scoring functions: `calculate_scores()` turns raw answers into per-dimension and overall percentages + a readiness level (`High` / `Moderate` / `Developing`); `summarize_recommendations()` picks the top recommendation for any dimension scoring below 70%. |
| `agent.py` | Chat response logic with a 3-tier fallback: **Gemini API → OpenAI API → rule-based keyword matcher** (`_rule_based_response`). Reads `GEMINI_API_KEY` / `OPENAI_API_KEY` from environment via `dotenv`. |
| `app.py` | CLI orchestration: role selection → question loop → score display → chatbot loop. Imports the three modules above directly (same process, same memory space). |
| `app.js` | Browser-side reimplementation of `QUESTIONS`, `RECOMMENDATIONS`, `calculateScores()`, and `chatbotResponse()` — a near-duplicate of the Python logic — plus DOM rendering and an optional fetch to an external chat API. |

### 2.2 Request flow (CLI)

The CLI path is a single local process with no network calls unless an LLM key is present:

1. `main()` prints the header and calls `select_role()`.
2. `ask_assessment_questions()` loops through `QUESTIONS`, validating A–D input.
3. `calculate_scores(answers)` averages per-dimension raw scores (0–3 scale), converts to percent, and derives an overall readiness level.
4. `show_results()` prints scores and calls `summarize_recommendations()`.
5. `run_chatbot()` loops, calling `chatbot_response()` per message, which tries Gemini, then OpenAI, then falls back to keyword rules.

### 2.3 Request flow (Web)

1. `init()` renders roles and questions into the DOM.
2. On form submit, `app.js` computes scores **client-side** using its own copy of the scoring logic and renders results + recommendations.
3. Chat messages are sent to `window.CHAT_API_URL + '/chat'` **if configured** (this is the one hook that anticipates a real backend); otherwise it falls back to the local JS rule-based responder.

### 2.4 Known architectural gaps (to resolve entering Phase 2)

- **Duplicated logic**: scoring and chatbot rules exist twice (Python and JS), which will drift as questions/recommendations evolve.
- **No backend/API**: `app.py` and `app.js` do not talk to each other; the web UI's `CHAT_API_URL` hook is unused until a server exists.
- **No persistence**: nothing is stored — required for Phase 2's "store responses, scores, and department data."
- **Secrets handling**: `agent.py` correctly keeps LLM calls server-side via `.env`, which is the right pattern to preserve once a backend exists (never call OpenAI/Gemini directly from `app.js`/the browser).
- **No role-specific question sets yet**: `role` is captured and passed into chat context, but all stakeholders currently answer the same 8 questions.

---

## 3. Phase 2 — Role-Adaptive AI Readiness Agent

**Goal:** one backend service that both the CLI and web client can call, adding role-specific questions, a RAG knowledge base, persistent storage, and a basic dashboard.

### 3.1 Target architecture

The key structural change is introducing a single **API service** as the shared source of truth, replacing the current duplicate-logic pattern. Both the existing `app.js` web client and a future CLI client become thin callers of the same API — exactly the pattern `app.js` already anticipates via `CHAT_API_URL`.

**Core services:**

1. **API layer** (e.g. FastAPI, since the codebase is already Python) exposing:
   - `GET /questions?role=` — role-specific question sets
   - `POST /assessment` — submit answers, get back scores + recommendations (server-side `assessment.py` logic, single source of truth)
   - `POST /chat` — role- and score-aware chatbot, matching the endpoint shape `app.js` already calls
   - `GET /dashboard/results` — retrieve stored results for the basic dashboard
2. **Agent/orchestration layer** — evolves `agent.py`'s existing Gemini/OpenAI-with-fallback pattern into a small ReAct-style loop: given a user question, role, and scores, the agent decides whether to (a) answer directly, (b) retrieve from the RAG knowledge base, or (c) fall back to rule-based responses if no LLM key is configured or the call fails.
3. **RAG knowledge base** — embeddings of the AI-readiness frameworks and papers reviewed in Phase 1 research (RAG, ReAct, Advanced RAG, plus higher-ed AI-readiness frameworks), stored in a vector store (e.g. pgvector alongside the relational data, or a lightweight vector DB) and queried before the LLM call to ground recommendations in source material.
4. **Persistence layer** — relational database (e.g. Postgres) storing:
   - `users`/`sessions` (role, department, timestamp)
   - `assessment_responses` (per-question answers)
   - `assessment_scores` (per-dimension + overall, denormalized for fast dashboard reads)
   - `chat_logs` (optional, for refining agent responses in Phase 3)
5. **Basic dashboard** — a simple read view (could be a route in the same web app) showing an individual's or session's score history, replacing the current "results" section which only shows the latest in-memory run.

### 3.2 Data model sketch

- `Role`: one of the 5 `STAKEHOLDER_ROLES` already defined in `framework.py`.
- `Question`: `id`, `text`, `dimension`, `choices` (A–D → value + text) — extended with an optional `role` filter so question sets can diverge by stakeholder group without duplicating the scoring math.
- `Dimension`: the 4 fixed categories (Governance & Policy, Systems & Infrastructure, Culture & Skills, Education & Training) — unchanged from Phase 1.
- `AssessmentResult`: `role`, `department`, `answers`, `dimension_scores`, `overall_score`, `level`, `created_at`.

### 3.3 Agent workflow (ReAct-style)

For a chat message, the agent should:
1. Take `message`, `role`, `scores` as input (same signature `chatbot_response()` already uses).
2. Retrieve relevant passages from the RAG knowledge base scoped to the dimensions the user is asking about or scoring low on.
3. Call the LLM (Gemini preferred, OpenAI fallback — preserving `agent.py`'s existing precedence) with retrieved context + role + scores.
4. If no LLM is configured or the call fails, fall back to the existing rule-based responder as a safety net (already implemented — keep it as the Phase 2 baseline, not something to throw away).
5. Log the exchange for later response-quality review (Phase 3 "test and refine agent responses").

---

## 4. Phase 3 — Organizational Readiness Platform

**Goal:** turn the single-agent, single-user prototype into a department/organization-level tool.

### 4.1 What's added on top of Phase 2

- **Aggregation layer**: roll up individual `AssessmentResult` rows by department/unit — average scores per dimension, per department, over time.
- **Reporting engine**: generate department-level and organization-level PDF/exportable reports (reusing the existing recommendation text as a base, expanded with aggregated data).
- **Cross-department comparison**: a view/query layer that ranks or compares departments by dimension, to surface where institutional investment is most needed.
- **Improvement roadmap generator**: sequences the existing `RECOMMENDATIONS` (already keyed by dimension) into a time-phased plan based on how far below threshold each department scores.
- **Visualizations**: charts for score distributions, trends over time, and department comparisons — layered onto the Phase 2 dashboard rather than replacing it.
- **Evaluation harness**: a way to replay `chat_logs` against updated prompts/RAG content to check for regressions before each release — formalizing Phase 2's "log the exchange" step into an actual test loop.

### 4.2 Non-functional considerations introduced here

- **Multi-tenancy / access control**: department-level data means role-based access (a department head shouldn't see another department's raw responses, only aggregates).
- **Data retention & anonymization**: individual assessment answers should be separable from identity once aggregated into department reports.
- **Scalability**: RAG queries and LLM calls should be async/queued if usage grows across many departments simultaneously.

---

## 5. Migration path summary

| Phase | Key shift |
|---|---|
| 1 → 2 | Collapse duplicated Python/JS scoring logic into one backend API; add persistence, role-specific questions, and a RAG-augmented agent behind the existing Gemini→OpenAI→rule-based fallback chain. |
| 2 → 3 | Add aggregation, reporting, and comparison on top of the same data model — no new core scoring logic needed, since `assessment.py`'s per-dimension structure already generalizes to "many results, grouped by department." |

The dimension model, question/choice structure, and fallback-chatbot pattern already built in Phase 1 are designed to carry through all three phases unchanged in shape — only their scope (single session → single role → whole organization) grows.

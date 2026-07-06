# AI Readiness Agent Prototype

A Phase 1 prototype for a Higher Education AI Readiness Agent. This prototype includes:

- A simple role-based assessment flow
- Initial readiness scoring across core dimensions
- A lightweight rule-based chatbot interface
- A basic architecture description for the prototype

## What is included

- `app.py`: CLI entrypoint and chatbot flow
- `assessment.py`: assessment engine and score calculation
- `framework.py`: stakeholder roles, readiness dimensions, and questions
- `architecture.md`: prototype architecture overview

## Getting started

1. Install Python 3.10+.
3. Run the CLI prototype (optional):

```bash
python app.py
```

4. Run the web UI prototype:

```bash
pip install -r requirements.txt
python web_app.py
```

Open http://127.0.0.1:5000 in your browser, choose a role, answer the assessment questions, and view results and the chat assistant.

## Prototype goals

- Validate concept for stakeholder-aware AI readiness assessment
- Capture initial readiness dimensions and scoring
- Provide tailored recommendations based on assessment results
- Enable further extension for research and RAG-based knowledge integration

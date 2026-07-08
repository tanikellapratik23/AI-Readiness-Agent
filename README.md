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

4. Run the web UI prototype locally:

```bash
pip install -r requirements.txt
python web_app.py
```

Open http://127.0.0.1:5000 in your browser to use the app locally.

## GitHub Pages hosting (static client-side demo)

This repository now includes a static client-side prototype under `docs/` that can be hosted on GitHub Pages. It reproduces the assessment scoring and chatbot behavior entirely in the browser, without a Python backend.

GitHub Actions are configured to deploy the `docs/` directory whenever you push to `main`.

To see the site after pushing, enable GitHub Pages for the repository (or wait for the Pages action to deploy). The URL will typically be:

```text
https://<your-github-username>.github.io/<repository-name>/
```

## Deploying to a real website

To expose the Flask app on a real domain later, deploy it to a hosting provider and use the `HOST` and `PORT` environment variables, for example:

```bash
HOST=0.0.0.0 PORT=80 python web_app.py
```

For production usage, run the Flask app behind a WSGI server such as Gunicorn or a cloud platform that supports Python apps. Then configure your domain name and HTTPS through the hosting provider.

## Prototype goals

- Validate concept for stakeholder-aware AI readiness assessment
- Capture initial readiness dimensions and scoring
- Provide tailored recommendations based on assessment results
- Enable further extension for research and RAG-based knowledge integration

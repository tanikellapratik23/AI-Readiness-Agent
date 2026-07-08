import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Gemini (Generative) API key (do NOT commit keys to the repo)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    import openai
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except Exception:
    openai = None

try:
    import requests
except Exception:
    requests = None


def _rule_based_response(text: str, role: str, scores: dict) -> str:
    if not text:
        return "Please type a question or ask for recommendations."
    if "what is ai readiness" in text or "ai readiness" in text:
        return "AI readiness measures how prepared your institution is to integrate AI responsibly across governance, infrastructure, culture, and training."
    if "governance" in text:
        return "Governance readiness is about policies, ethical frameworks, and clear guidance for stakeholders on responsible AI use."
    if "infrastructure" in text or "systems" in text:
        return "Infrastructure readiness covers access to AI tools, secure systems, and data practices that support teaching, research, and administration."
    if "training" in text or "education" in text or "skills" in text:
        return "Training readiness means providing AI literacy, role-specific guidance, and continuous support for students, faculty, and staff."
    if "recommend" in text or "improve" in text or "next step" in text:
        return "Evaluate the dimensions where your score is below 70% and prioritize governance, infrastructure, or training improvements accordingly."
    if "score" in text or "result" in text:
        return f"Your current score is {scores.get('overall', {}).get('percent', 'N/A')}% with readiness level {scores.get('overall', {}).get('level', 'N/A')}."
    if "student" in text or "faculty" in text or "leadership" in text or "business" in text or "communications" in text:
        return f"As a {role}, focus on how your role-specific needs align with governance, infrastructure, culture, and training in your unit." 
    return "This prototype can answer questions about readiness dimensions, scores, and recommendations. Try asking about governance, infrastructure, or training."


def chatbot_response(message: str, role: str, scores: dict) -> str:
    text = (message or "").strip().lower()

    # If Google Gemini is configured, prefer it for LLM responses (server-side only)
    if GEMINI_API_KEY and requests:
        try:
            gem_resp = _gemini_response(message, role, scores)
            if gem_resp:
                return gem_resp
        except Exception:
            pass

    # If OpenAI is configured, attempt an LLM-backed response with context
    if openai and OPENAI_API_KEY:
        try:
            system_prompt = (
                "You are a helpful assistant that provides concise, actionable guidance about higher-education AI readiness. "
                "Use the provided role and scores to tailor recommendations."
            )
            user_context = f"role: {role}\nscores: {scores}\nquestion: {message}"
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_context},
                ],
                max_tokens=300,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception:
            # Fall back to rule-based if API call fails
            return _rule_based_response(text, role, scores)

    # Default: rule-based response
    return _rule_based_response(text, role, scores)
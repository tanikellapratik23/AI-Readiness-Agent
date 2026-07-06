import sys
from assessment import calculate_scores, summarize_recommendations
from framework import STAKEHOLDER_ROLES, QUESTIONS
from agent import chatbot_response


def print_header():
    print("\n=== Higher Education AI Readiness Agent Prototype ===\n")
    print("This prototype captures Phase 1 readiness assessment and a simple role-aware chatbot interface.")


def select_role():
    print("Select your role:")
    for idx, role in enumerate(STAKEHOLDER_ROLES, start=1):
        print(f"  {idx}. {role}")
    while True:
        choice = input("Enter the number for your role: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(STAKEHOLDER_ROLES):
            return STAKEHOLDER_ROLES[int(choice) - 1]
        print("Invalid selection. Please choose a valid role number.")


def ask_assessment_questions():
    answers = {}
    print("\nAnswer the following readiness questions using A, B, C, or D.")
    for question in QUESTIONS:
        print(f"\n{question['id']}. {question['text']}")
        for key, (_, text) in question["choices"].items():
            print(f"  {key}. {text}")
        while True:
            answer = input("Your choice: ").strip().upper()
            if answer in question["choices"]:
                answers[question["id"]] = answer
                break
            print("Please enter A, B, C, or D.")
    return answers


def show_results(role: str, scores: dict):
    print("\n=== Assessment Results ===")
    print(f"Role: {role}")
    print(f"Overall readiness level: {scores['overall']['level']}")
    print(f"Overall score: {scores['overall']['percent']}%")
    print("\nDimension scores:")
    for dimension, value in scores["dimensions"].items():
        print(f"  {dimension}: {value['percent']}%")
    recommendations = summarize_recommendations(scores)
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"  - {rec}")


# Chatbot logic is provided by `agent.py` so both CLI and web UI can reuse it.


def run_chatbot(role: str, scores: dict):
    print("\n=== Chatbot Assistant ===")
    print("Ask a question about AI readiness, or type 'exit' to quit.")
    while True:
        message = input("You: ").strip()
        if message.lower() in {"exit", "quit", "done"}:
            print("Exiting chatbot. Thank you.")
            break
        response = chatbot_response(message, role, scores)
        print(f"Agent: {response}")


def main():
    print_header()
    role = select_role()
    answers = ask_assessment_questions()
    scores = calculate_scores(answers)
    show_results(role, scores)
    run_chatbot(role, scores)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye.")
        sys.exit(0)

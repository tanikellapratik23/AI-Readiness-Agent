from statistics import mean
from framework import DIMENSIONS, QUESTIONS, RECOMMENDATIONS


def normalize_score(value: int) -> float:
    return round((value / 3) * 100, 1)


def calculate_scores(answers: dict) -> dict:
    dimension_scores = {dimension: [] for dimension in DIMENSIONS}
    for question_id, choice_key in answers.items():
        question = next((q for q in QUESTIONS if q["id"] == question_id), None)
        if question is None:
            continue
        value, _ = question["choices"][choice_key]
        dimension_scores[question["dimension"]].append(value)

    dimension_summary = {}
    for dimension, values in dimension_scores.items():
        if values:
            average = mean(values)
            dimension_summary[dimension] = {
                "raw": round(average, 2),
                "percent": normalize_score(average)
            }
        else:
            dimension_summary[dimension] = {
                "raw": 0,
                "percent": 0.0
            }

    overall = mean([summary["raw"] for summary in dimension_summary.values()])
    return {
        "dimensions": dimension_summary,
        "overall": {
            "raw": round(overall, 2),
            "percent": normalize_score(overall),
            "level": readiness_level(overall)
        }
    }


def readiness_level(raw_average: float) -> str:
    if raw_average >= 2.5:
        return "High"
    if raw_average >= 1.5:
        return "Moderate"
    return "Developing"


def summarize_recommendations(scores: dict) -> list:
    recommendations = []
    for dimension, dimension_scores in scores["dimensions"].items():
        if dimension_scores["percent"] < 70:
            recommendations.append(
                f"{dimension}: {RECOMMENDATIONS[dimension][0]}"
            )
    if not recommendations:
        recommendations.append("Your institution shows strong readiness indicators. Continue reinforcing governance, infrastructure, culture, and training.")
    return recommendations

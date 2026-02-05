import re

def assess_clause_risk(clause):
    clause_lower = clause.lower()

    # --- HIGH RISK ---
    if "terminate" in clause_lower and ("without notice" in clause_lower or "without cause" in clause_lower):
        return "High"

    if "shall not be liable" in clause_lower:
        return "High"

    if "no liability" in clause_lower:
        return "High"

    if "zero liability" in clause_lower:
        return "High"

    if "unlimited liability" in clause_lower:
        return "High"

    if "non-refundable" in clause_lower:
        return "High"

    if "sole discretion" in clause_lower:
        return "High"

    if "may not terminate" in clause_lower:
        return "High"

    if "non-compete" in clause_lower:
        return "High"

    if "penalty" in clause_lower:
        return "High"

    # --- MEDIUM RISK ---
    if "indemnify" in clause_lower:
        return "Medium"

    if "governed by" in clause_lower:
        return "Medium"

    if "auto-renew" in clause_lower:
        return "Medium"

    if "lock-in" in clause_lower:
        return "Medium"

    if "90 days" in clause_lower or "120 days" in clause_lower:
        return "Medium"

    return "Low"


def compute_contract_risk(clauses):

    weights = {
        "Low": 1,
        "Medium": 3,
        "High": 6
    }

    if not clauses:
        return {
            "clause_risks": [],
            "composite_score": 0,
            "summary": "No clauses detected.",
            "high_risk_clauses": []
        }

    clause_risks = []
    total_score = 0
    high_count = 0
    critical_flag = False

    for clause in clauses:
        risk = assess_clause_risk(clause)
        clause_risks.append({"text": clause, "risk": risk})
        total_score += weights[risk]

        if risk == "High":
            high_count += 1

        if any(x in clause.lower() for x in [
            "non-refundable",
            "sole discretion",
            "zero liability",
            "may not terminate",
            "unlimited liability"
        ]):
            critical_flag = True

    # ----------------------------
    # PROFESSIONAL RATIO SCORING
    # ----------------------------

    max_possible = len(clauses) * 6
    raw_ratio = total_score / max_possible   # 0 to 1 scale

    # Controlled escalation on ratio
    if high_count == 0:
        risk_multiplier = 1
    elif high_count == 1:
        risk_multiplier = 1.1
    elif high_count == 2:
        risk_multiplier = 1.25
    elif high_count == 3:
        risk_multiplier = 1.4
    else:
        risk_multiplier = 1.6

    raw_ratio *= risk_multiplier

    # Small bump for critical patterns
    if critical_flag:
        raw_ratio += 0.08

    # Severe stacking floor (but not instant 10)
    if high_count >= 3:
        raw_ratio = max(raw_ratio, 0.75)

    # Final clamp
    raw_ratio = min(raw_ratio, 1)

    composite_score = round(raw_ratio * 10, 2)

    # Risk level interpretation
    if composite_score >= 8:
        level = "High Risk"
    elif composite_score >= 5:
        level = "Moderate Risk"
    else:
        level = "Low Risk"

    summary = f"""
This contract is classified as {level}.
Risk scoring is based on clause-level weighting,
stacked high-risk detection, and critical pattern escalation.
"""

    return {
        "clause_risks": clause_risks,
        "composite_score": composite_score,
        "summary": summary,
        "high_risk_clauses": [c["text"] for c in clause_risks if c["risk"] == "High"]
    }

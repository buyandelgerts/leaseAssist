# tools/income_tool.py
from crewai.tools import tool

@tool("IncomeCalculatorTool")
def income_calculator_tool(
    monthly_income: float,
    monthly_debts: float,
    state: str
) -> str:
    """
    Calculates rental affordability using the 30% rule and DTI ratio.
    Returns a verdict (ELIGIBLE / BORDERLINE / NOT ELIGIBLE) and max budget.

    Args:
        monthly_income: Gross monthly income in USD
        monthly_debts: Total monthly debt payments (car, student loans, etc.)
        state: US state abbreviation (e.g. 'CA', 'TX', 'NY')
    """
    # Step 1: 30% rule — max rent should be 30% of gross monthly income
    max_rent_30pct = monthly_income * 0.30

    # Step 2: Debt-to-income ratio — total debts + rent should be under 43%
    remaining_for_rent = (monthly_income * 0.43) - monthly_debts
    max_rent_dti = max(0, remaining_for_rent)

    # Step 3: Take the lower of the two as the safe budget
    safe_budget = min(max_rent_30pct, max_rent_dti)

    # Step 4: State-specific income multiplier requirements
    # Many landlords require income = 2.5x to 3x the monthly rent
    state_multipliers = {
        "CA": 2.5, "NY": 3.0, "TX": 2.5, "FL": 2.5,
        "WA": 2.5, "IL": 2.5, "MA": 3.0, "default": 2.5
    }
    multiplier = state_multipliers.get(state.upper(), state_multipliers["default"])
    max_rent_income_req = monthly_income / multiplier

    # Final max affordable rent
    final_budget = min(safe_budget, max_rent_income_req)

    # Verdict
    dti_ratio = (monthly_debts / monthly_income) * 100 if monthly_income > 0 else 100
    if dti_ratio > 50:
        verdict = "NOT ELIGIBLE"
        reason = f"Debt-to-income ratio is {dti_ratio:.1f}% — too high (max 43%)"
    elif final_budget < 600:
        verdict = "NOT ELIGIBLE"
        reason = "Affordable budget is below minimum rental threshold"
    elif dti_ratio > 35:
        verdict = "BORDERLINE"
        reason = f"DTI is {dti_ratio:.1f}%. Manageable but tight. Guarantor recommended."
    else:
        verdict = "ELIGIBLE"
        reason = f"Income and debt levels meet {state.upper()} rental standards"

    return f"""
=== ELIGIBILITY REPORT ===
Verdict: {verdict}
Reason: {reason}

Income Details:
  Monthly gross income: ${monthly_income:,.2f}
  Monthly debts: ${monthly_debts:,.2f}
  Debt-to-income ratio: {dti_ratio:.1f}%

Affordability:
  Max rent (30% rule): ${max_rent_30pct:,.2f}
  Max rent (DTI rule): ${max_rent_dti:,.2f}
  Max rent ({state} income req {multiplier}x): ${max_rent_income_req:,.2f}
  SAFE BUDGET RANGE: $600 – ${final_budget:,.2f}/month

State: {state.upper()}
"""
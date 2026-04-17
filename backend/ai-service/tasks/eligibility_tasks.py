# tasks/eligibility_tasks.py
from crewai import Task

def create_eligibility_task(agent):
    return Task(
        description="""
        A tenant has submitted their financial details for eligibility screening.

        Tenant details:
        - Monthly gross income: ${monthly_income}
        - Monthly debt payments: ${monthly_debts}
        - State: {state}
        - Desired rent budget: ${desired_budget}

        Your job:
        1. Run the IncomeCalculatorTool with the provided figures
        2. Determine if the tenant is ELIGIBLE, BORDERLINE, or NOT ELIGIBLE
        3. Provide their maximum safe monthly rent
        4. Give 2–3 actionable recommendations if borderline or ineligible
        """,
        expected_output="""
        A structured report containing:
        - Verdict (ELIGIBLE / BORDERLINE / NOT ELIGIBLE)
        - Maximum affordable rent
        - DTI ratio
        - 2–3 recommendations if applicable
        """,
        agent=agent,
        output_file="outputs/eligibility_report.txt"
    )
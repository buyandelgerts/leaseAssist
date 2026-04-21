from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any
import json

class EligibilityInput(BaseModel):
    applicant_data: dict[str, Any] = Field(
        description="Applicant attributes to evaluate"
    )
    context_documents: list[dict] = Field(
        default=[],
        description="Supporting documents from vector search to inform the decision"
    )


class EligibilityCalculatorTool(BaseTool):
    name: str = "eligibility_calculator"
    description: str = (
        "Evaluate whether an applicant meets eligibility criteria by applying "
        "business rules against their data and any supporting context documents. "
        "Returns a structured eligibility decision with reasons."
    )
    args_schema: type[BaseModel] = EligibilityInput

    # ── Customize this rules dict for your domain ──────────────────────────
    RULES: dict[str, Any] = {
        "required_fields": ["monthly_income", "monthly_debts", "desired_budget", "state"],
        "minimum_monthly_income": 3000,
        "maximum_debt_to_income_ratio": 0.50,
        "maximum_budget_to_income_ratio": 0.40,
    }

    def _run(
        self,
        applicant_data: dict[str, Any],
        context_documents: list[dict] | None = None,
    ) -> str:
        context_documents = context_documents or []
        reasons: list[str] = []
        applied_rules: list[str] = []
        passed = 0
        total = 0

        # Rule 1: required fields
        for field in self.RULES["required_fields"]:
            total += 1
            applied_rules.append(f"required_field:{field}")
            if field in applicant_data and applicant_data[field] not in (None, ""):
                passed += 1
            else:
                reasons.append(f"Missing required field: '{field}'")

        # Rule 2: minimum monthly income
        total += 1
        applied_rules.append("minimum_income")
        monthly_income = applicant_data.get("monthly_income", 0)
        if isinstance(monthly_income, (int, float)) and monthly_income >= self.RULES["minimum_monthly_income"]:
            passed += 1
        else:
            reasons.append(
                f"Monthly income below required minimum of ${self.RULES['minimum_monthly_income']:,}."
            )

        # Rule 3: debt-to-income ratio
        total += 1
        applied_rules.append("maximum_debt_to_income_ratio")
        monthly_debts = applicant_data.get("monthly_debts", 0)
        debt_ratio = (monthly_debts / monthly_income) if monthly_income else 1.0
        if isinstance(monthly_debts, (int, float)) and debt_ratio <= self.RULES["maximum_debt_to_income_ratio"]:
            passed += 1
        else:
            reasons.append(
                f"Monthly debts exceed {int(self.RULES['maximum_debt_to_income_ratio'] * 100)}% of reported income."
            )

        # Rule 4: desired budget affordability
        total += 1
        applied_rules.append("maximum_budget_to_income_ratio")
        desired_budget = applicant_data.get("desired_budget", 0)
        budget_ratio = (desired_budget / monthly_income) if monthly_income else 1.0
        if isinstance(desired_budget, (int, float)) and budget_ratio <= self.RULES["maximum_budget_to_income_ratio"]:
            passed += 1
        else:
            reasons.append(
                f"Desired budget is above {int(self.RULES['maximum_budget_to_income_ratio'] * 100)}% of monthly income."
            )

        confidence = round(passed / total, 2) if total > 0 else 0.0
        is_eligible = confidence >= 0.75

        if not reasons:
            reasons.append("All eligibility criteria met.")

        return json.dumps({
            "is_eligible": is_eligible,
            "confidence_score": confidence,
            "reasons": reasons,
            "applied_rules": applied_rules,
            "recommendation": (
                "Approve — applicant meets all criteria."
                if is_eligible
                else "Deny — see reasons above."
            ),
        }, indent=2)
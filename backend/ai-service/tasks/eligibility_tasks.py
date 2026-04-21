from crewai import Task
from crewai import Agent
from typing import Any, Optional
import json

def create_eligibility_task(
    agent: Agent,
    applicant_data: dict[str, Any],
    context_task: Optional[Task] = None,  # optional chained output from search task
) -> Task:
    applicant_data_text = json.dumps(applicant_data, indent=2, default=str).replace("{", "(").replace("}", ")")

    task_kwargs = {}
    if context_task is not None:
        task_kwargs["context"] = [context_task]

    return Task(
        description=(
            "Using the search results from the previous task and the applicant data below, "
            "determine whether the applicant is eligible.\n\n"
            f"APPLICANT DATA:\n{applicant_data_text}\n\n"
            "Steps:\n"
            "1. Review the context documents from the search task.\n"
            "2. Run the eligibility_calculator tool with the applicant data.\n"
            "3. Cross-reference the tool output with any policy details in the documents.\n"
            "4. Return a final eligibility decision with reasons and recommendation."
        ),
        expected_output=(
            "A JSON object containing: 'is_eligible' (bool), 'confidence_score' (0-1), "
            "'reasons' (list), 'applied_rules' (list), and 'recommendation' (string)."
        ),
        agent=agent,
        **task_kwargs,
    )
from crewai import Agent
from tools.eligibility_tool import EligibilityCalculatorTool

def create_eligibility_agent() -> Agent:
    return Agent(
        role="Eligibility Assessment Specialist",
        goal=(
            "Determine whether an applicant is eligible based on their data "
            "and the relevant policy documents provided by the search agent."
        ),
        backstory=(
            "You are a meticulous compliance officer who evaluates applicants "
            "against a defined set of eligibility rules. You use both structured "
            "applicant data and contextual documents to make fair, well-reasoned "
            "decisions. You always explain your reasoning clearly."
        ),
        tools=[EligibilityCalculatorTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
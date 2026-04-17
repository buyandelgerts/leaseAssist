# crew.py
from crewai import Crew, Process
from agents.eligibility_agent import create_eligibility_agent
from agents.property_agent import create_property_agent
from agents.contract_agent import create_contract_agent
from agents.chatbot_agent import create_chatbot_agent
from tasks.eligibility_tasks import create_eligibility_task
from tasks.property_tasks import create_property_task
from tasks.contract_tasks import create_contract_task
from tasks.chatbot_tasks import create_chatbot_task

def run_eligibility(inputs: dict) -> str:
    """Runs only the eligibility calculator crew."""
    agent = create_eligibility_agent()
    task = create_eligibility_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True
    )
    return crew.kickoff(inputs=inputs)

def run_property_matcher(inputs: dict) -> str:
    """Runs only the property matcher crew."""
    agent = create_property_agent()
    task = create_property_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True
    )
    return crew.kickoff(inputs=inputs)

def run_contract_analyzer(inputs: dict) -> str:
    """Runs only the contract analyzer crew. Includes HITL on task."""
    agent = create_contract_agent()
    task = create_contract_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True
    )
    return crew.kickoff(inputs=inputs)

def run_chatbot(inputs: dict) -> str:
    """Runs only the chatbot crew."""
    agent = create_chatbot_agent()
    task = create_chatbot_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True
    )
    return crew.kickoff(inputs=inputs)
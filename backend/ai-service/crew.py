# crew.py
from crewai import Crew, Process
from agents.eligibility_agent import create_eligibility_agent
from agents.property_agent import create_property_agent
from agents.contract_agent import create_contract_agent
from agents.chatbot_agent import create_chatbot_agent
from agents.lease_analyzer_agents import (
    web_scraper_agent,
    clause_extractor_agent,
    red_flag_detector_agent,
    comparison_agent,
    negotiation_advisor_agent,
)
from tasks.eligibility_tasks import create_eligibility_task
from tasks.property_tasks import create_property_task
from tasks.contract_tasks import create_contract_task
from tasks.chatbot_tasks import create_chatbot_task
from tasks.lease_analyzer_tasks import (
    scrape_task,
    extract_task,
    red_flag_task,
    compare_task,
    negotiate_task,
    on_task_complete,
)

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

def run_lease_analyzer(inputs: dict) -> str:
    """Runs the full lease analyzer crew (6 agents, 6 tasks)."""
    scraper = web_scraper_agent()
    extractor = clause_extractor_agent()
    detector = red_flag_detector_agent()
    comparator = comparison_agent()
    negotiator = negotiation_advisor_agent()

    t_scrape = scrape_task(scraper)
    t_extract = extract_task(extractor, t_scrape)
    t_red_flag = red_flag_task(detector, t_extract)
    t_compare = compare_task(comparator, t_extract, t_red_flag)
    t_negotiate = negotiate_task(negotiator, t_extract, t_red_flag, t_compare)

    crew = Crew(
        agents=[scraper, extractor, detector, comparator, negotiator],
        tasks=[t_scrape, t_extract, t_red_flag, t_compare, t_negotiate],
        process=Process.sequential,
        verbose=True,
        task_callback=on_task_complete
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
# crew.py
import os
import sys

from crewai import Crew, Process
from mcp import StdioServerParameters

from agents.chatbot_agent import (
    create_chatbot_manager_agent,
    create_search_sub_agent,
    create_router_agent,
    create_general_qa_agent,
)
from agents.eligibility_agent import create_eligibility_agent
from agents.property_agent import create_property_agent
from agents.contract_agent import create_contract_agent
from agents.lease_analyzer_agents import (
    web_scraper_agent,
    clause_extractor_agent,
    red_flag_detector_agent,
    comparison_agent,
    negotiation_advisor_agent,
)
from tasks.chatbot_tasks import create_chatbot_manager_task
from tasks.eligibility_tasks import create_eligibility_task
from tasks.property_tasks import create_property_task
from tasks.contract_tasks import create_contract_task
from tasks.lease_analyzer_tasks import (
    scrape_task,
    extract_task,
    red_flag_task,
    compare_task,
    negotiate_task,
    on_task_complete,
)

from agents.tour_request_agent import create_tour_request_agent
from tasks.send_tour_request_task import create_send_tour_request_task
from db.vector_store import similarity_search

_MCP_SERVER = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(__file__), "mcp_server.py")],
    env={**os.environ},
)


def run_eligibility(inputs: dict) -> str:
    agent = create_eligibility_agent()
    task = create_eligibility_task(agent=agent, applicant_data=inputs)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True,
    )
    return crew.kickoff(inputs=inputs)


def run_property_matcher(inputs: dict) -> str:
    agent = create_property_agent(_MCP_SERVER)
    task = create_property_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True,
    )
    return crew.kickoff(inputs=inputs)


def run_contract_analyzer(inputs: dict) -> str:
    agent = create_contract_agent(_MCP_SERVER)
    task = create_contract_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True,
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

def run_chatbot(inputs: dict) -> dict:
    import json as _json

    manager = create_chatbot_manager_agent(_MCP_SERVER)
    search_agent = create_search_sub_agent(_MCP_SERVER)
    router = create_router_agent()
    general_qa = create_general_qa_agent()

    manager_task = create_chatbot_manager_task()

    crew = Crew(
        agents=[search_agent, router, general_qa],
        tasks=[manager_task],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )
    result = crew.kickoff(inputs=inputs)

    if hasattr(result, "json_dict") and result.json_dict:
        return result.json_dict

    # Hierarchical mode sometimes returns valid JSON as the raw string
    raw_str = str(result).strip()
    try:
        parsed = _json.loads(raw_str)
        if isinstance(parsed, dict) and "type" in parsed:
            return parsed
    except (_json.JSONDecodeError, ValueError):
        pass

    return {"type": "text", "message": raw_str}


def run_search_agent(inputs: dict) -> dict:
    raw_query = (inputs.get("query") or "").strip()
    city = (inputs.get("city") or "").strip()
    state = (inputs.get("state") or "").strip()
    raw_limit = inputs.get("limit")
    limit = int(raw_limit) if raw_limit not in (None, "") else None

    if not city or not state:
        raise ValueError("Both city and state are required for search.")

    results = similarity_search(
        query=raw_query if raw_query else None,
        city=city,
        state=state,
        limit=limit,
    )
    return {
        "query": raw_query if raw_query else None,
        "city": city,
        "state": state,
        "total_found": len(results),
        "results": results,
    }


def run_eligibility_tasks(applicant_data: dict, search_output: str) -> str:
        agent = create_eligibility_agent()
        task = create_eligibility_task(
            agent=agent,
            applicant_data=applicant_data,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return str(result)

def run_send_tour_request(inputs: dict) -> str:
    agent = create_tour_request_agent(_MCP_SERVER)
    task = create_send_tour_request_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True,
    )
    return crew.kickoff(inputs=inputs)
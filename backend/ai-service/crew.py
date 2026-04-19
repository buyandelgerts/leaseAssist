# crew.py
import os
import sys

from crewai import Crew, Process
from mcp import StdioServerParameters

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

_MCP_SERVER = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(__file__), "mcp_server.py")],
    env={**os.environ},
)


def run_eligibility(inputs: dict) -> str:
    agent = create_eligibility_agent(_MCP_SERVER)
    task = create_eligibility_task(agent)
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
        task_callback=on_task_complete,
    )
    return crew.kickoff(inputs=inputs)


def run_chatbot(inputs: dict) -> str:
    ctx = inputs.get("session_context")
    if ctx is not None and hasattr(ctx, "model_dump"):
        ctx_data = ctx.model_dump(exclude_none=True)
        if ctx_data:
            lines = []
            if ctx_data.get("eligibility_result"):
                lines.append(f"Eligibility result: {ctx_data['eligibility_result']}")
            if ctx_data.get("lease_analysis"):
                lines.append(f"Lease analysis:\n{ctx_data['lease_analysis']}")
            inputs["session_context"] = "\n".join(lines) if lines else "No prior results available."
        else:
            inputs["session_context"] = "No prior results available."
    elif not inputs.get("session_context"):
        inputs["session_context"] = "No prior results available."

    agent = create_chatbot_agent(_MCP_SERVER)
    task = create_chatbot_task(agent)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        memory=True,
        verbose=True,
    )
    return crew.kickoff(inputs=inputs)

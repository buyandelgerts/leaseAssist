# agents/lease_analyzer_agents.py
from crewai import Agent


def web_scraper_agent():
    return Agent(
        role="Lease Data Extractor",
        goal="Extract lease-related information from raw text input.",
        backstory=(
            "You are an expert at extracting lease information from text. "
            "You extract all relevant details: rent, deposit, lease terms, "
            "restrictions, amenities, pet policies, and any other lease-related information."
        ),
        verbose=True,
        max_iter=3
    )


def clause_extractor_agent():
    return Agent(
        role="Lease Clause Extractor",
        goal="Parse raw lease terms and organize them into clear, structured categories.",
        backstory=(
            "You are a legal assistant specializing in residential leases. "
            "You take messy lease terms and organize them into clean categories: "
            "rent, deposit, restrictions, penalties, landlord rights, and tenant obligations."
        ),
        verbose=True,
        max_iter=3
    )


def red_flag_detector_agent():
    return Agent(
        role="Lease Red Flag Detector",
        goal="Identify unfair, unusual, or potentially illegal clauses in a lease agreement.",
        backstory=(
            "You are a tenant rights advocate with deep knowledge of landlord-tenant laws "
            "across US states. You have helped thousands of renters spot problematic lease "
            "clauses before they sign. You know common legal limits on deposits, notice periods, "
            "and tenant rights by state."
        ),
        verbose=True,
        max_iter=3
    )


def comparison_agent():
    return Agent(
        role="Market Comparison Analyst",
        goal="Compare lease terms against typical market standards for the given city.",
        backstory=(
            "You are a real estate market analyst who tracks rental trends across major US cities. "
            "You know typical rent ranges, standard deposit amounts, common lease restrictions, "
            "and what is considered normal vs. unusual for each market."
        ),
        verbose=True,
        max_iter=3
    )


def negotiation_advisor_agent():
    return Agent(
        role="Lease Negotiation Advisor",
        goal="Provide specific, actionable negotiation points and draft a professional email to the landlord.",
        backstory=(
            "You are an experienced tenant negotiation coach. You help renters negotiate "
            "better lease terms by prioritizing what to push back on, what to accept, "
            "and how to communicate professionally with landlords to get results."
        ),
        verbose=True,
        max_iter=3
    )



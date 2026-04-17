# agents/property_agent.py
from crewai import Agent
from tools.property_search_tool import property_search_tool
from tools.property_filter_tool import property_filter_tool

def create_property_agent():
    return Agent(
        role="Property Matching Specialist",
        goal=(
            "Find the top 3 best-matching rental properties based on the "
            "tenant's budget, location preference, bedroom count, and amenities. "
            "Rank results by match score. Never suggest unavailable properties."
        ),
        backstory=(
            "You are an experienced real estate agent who has helped over 500 "
            "tenants find their perfect rental. You know how to filter listings "
            "by price, location, size, and features. You are honest about "
            "trade-offs and always show real, available units only."
        ),
        tools=[property_search_tool, property_filter_tool],
        memory=True,
        verbose=True,
        max_iter=5
    )
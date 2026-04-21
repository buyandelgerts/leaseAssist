from crewai import Agent


def create_property_agent(server):
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
        mcps=[server],
        memory=True,
        verbose=True,
        max_iter=5,
    )

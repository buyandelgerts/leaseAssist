# tasks/property_tasks.py
from crewai import Task

def create_property_task(agent):
    return Task(
        description="""
        A qualified tenant is looking for a rental property.

        Search criteria:
        - City: {city}
        - Maximum budget: ${max_budget}/month
        - Minimum bedrooms: {min_beds}
        - Has pets: {pet_friendly}
        - Special requirements: {special_requirements}

        Your job:
        1. Use PropertySearchTool to find matching available properties
        2. Rank the results by match score
        3. Return the top 3 with full details
        4. Write a brief 1-line recommendation note for each property
        """,
        expected_output="""
        Top 3 property matches with:
        - Address, rent, size, amenities
        - Match score (0-100)
        - One-line recommendation note per property
        """,
        agent=agent,
        output_file="outputs/property_matches.txt"
    )
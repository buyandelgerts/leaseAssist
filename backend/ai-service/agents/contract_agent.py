from crewai import Agent


def create_contract_agent(server):
    return Agent(
        role="Lease Contract Analyst",
        goal=(
            "Analyze a lease contract and identify all red flags (tenant-unfavorable "
            "clauses) and green flags (tenant-favorable protections) based on the "
            "laws of the specified US state. Always cite which law applies."
        ),
        backstory=(
            "You are a real estate paralegal specializing in tenant rights law "
            "across all 50 US states. You have reviewed over 2,000 lease "
            "agreements. You know every predatory clause and every tenant "
            "protection law. You never give legal advice — you analyze and flag."
        ),
        mcps=[server],
        memory=True,
        verbose=True,
        max_iter=6,
    )

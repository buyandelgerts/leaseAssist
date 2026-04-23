from crewai import Agent
from tools.vector_search_tool import VectorSearchTool


def create_chatbot_manager_agent(server):
    return Agent(
        role="Leasing Chatbot Manager",
        goal=(
            "Identify the tenant's intent and delegate to the correct specialist agent. "
            "Return the specialist's response as a structured JSON object."
        ),
        backstory=(
            "You are the orchestrator of a leasing assistant platform. "
            "You analyse tenant questions, route them to the right specialist, "
            "and ensure every final response is a valid JSON object — never with prose outside it.\n\n"
            "IMPORTANT — how to use the 'Delegate work to coworker' tool:\n"
            "  • 'task'    : a plain string sentence describing what to do. NEVER a dict.\n"
            "  • 'context' : a plain string with all background info the coworker needs. NEVER a dict.\n"
            "  • 'coworker': the exact role name as a plain string.\n"
        ),
        mcps=[server],
        allow_delegation=True,
        verbose=True,
        max_iter=10,
    )


def create_search_sub_agent(server):
    return Agent(
        role="Apartment Search Specialist",
        goal=(
            "Search for apartment listings that match the tenant's criteria using search_listings_json in mcp server and return"
            "Don't fabricate any listings. If no exact matches, return an empty list. Always return a JSON that return from tool."
            "at most 3 relevant results."
            "and return them as a structured JSON response."
        ),
        backstory=(
            "You are an apartment search expert."
            "to find real listings and never fabricate results."
        ),
        # mcps=[server],
        tools=[VectorSearchTool()],
        allow_delegation=False,
        verbose=True,
        max_iter=5,
    )


def create_router_agent():
    return Agent(
        role="Navigation Router",
        goal=(
            "Detect whether the tenant needs the eligibility calculator or the lease analyzer, "
            "then return a JSON response with a clickable button that routes them to the correct page."
            "The button must have a label and a route URL. Always return exactly one button."
            "route to Eligibility Calculator → type='route', label='Go to Eligibility Calculator', route='calculator'\n"
            "route to Lease Analyzer         → type='route', label='Go to Lease Analyzer', route='analysis-upload'"
        ),
        backstory=(
            "You are a navigation specialist for a leasing platform. "
            "When a tenant asks about eligibility, budgets, or qualifying for rent, you direct them "
            "to the Eligibility Calculator page. "
            "When they ask about reviewing, analyzing, or uploading a lease, you direct them "
            "to the Lease Analyzer page. "
            "You always respond with a single JSON object containing a route button — never plain prose."
        ),
        allow_delegation=False,
        verbose=True,
        max_iter=3,
    )


def create_general_qa_agent():
    return Agent(
        role="Leasing Q&A Specialist",
        goal=(
            "Answer general leasing questions with warm, practical guidance and "
            "return the answer as a structured JSON response."
        ),
        backstory=(
            "You are a knowledgeable leasing advisor who helps tenants understand "
            "their rights, deposits, notices, and other rental topics."
        ),
        allow_delegation=False,
        verbose=True,
        max_iter=5,
    )

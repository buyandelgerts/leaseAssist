# tasks/chatbot_tasks.py
from crewai import Task


def create_chatbot_task(agent):
    return Task(
        description="""
        A tenant has a question. Determine the intent and use the right tool.

        Tenant name: {tenant_name}
        User question: {user_question}
        Conversation history: {conversation_history}

        Session context (results from prior app actions):
        {session_context}

        Intent routing — pick the matching approach:

        1. PROPERTY SEARCH: If the user asks about apartments, rentals, or properties
           (e.g. "find me a 2-bed in Austin") → use ListingSearchTool with their query.

        2. LEASE LAW / CLAUSE QUESTION: If the user asks about a lease clause, security
           deposit, entry notice, rent increase, or tenant rights in a specific state
           → use StateLawTool with the relevant state and topic.

        3. PROCESS QUESTION: If the user asks about application steps, tenant rights
           in general, late rent, or pet policies → use LeasingKnowledgeBaseTool.

        4. SESSION SUMMARY: If the user asks "what's my eligibility?" or "summarize my
           results" → read session_context and explain it clearly. If no results exist
           yet, prompt them to run the calculator or lease analyzer.

        5. GUIDED NEGOTIATION: If the user says "walk me through my red flags" or
           "help me negotiate" → extract lease flags from session_context and walk
           through each one, explaining what law it may violate and how to negotiate it.

        Respond in 3–5 sentences. Be warm, practical, and cite your source.
        """,
        expected_output="""
        A helpful, concise response that:
        - Directly answers the question using the right tool or session context
        - Cites the source (e.g. "TX tenant law states...", "From your lease analysis...")
        - Ends with a relevant follow-up offer
        """,
        agent=agent,
    )
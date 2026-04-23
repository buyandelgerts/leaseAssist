# tasks/chatbot_tasks.py
from crewai import Task

from models.schema import ChatbotResponse


# def create_search_task(agent):
#     return Task(
#         description="""
#         Search for apartment listings based on the tenant's request.

#         Tenant name   : {tenant_name}
#         User question : {user_question}

#         Steps:
#           1. Extract city, state (infer from city if not stated), and
#              max_budget (if mentioned) from the question.
#           2. Call the MCP tool `search_listings_json` with those parameters.
#           3. Parse the returned JSON array into apartment objects.

#         Return exactly (type MUST be the string "apartments"):
#           {{
#             "type": "apartments",
#             "message": "Here are <N> residences in <city>, <state> that match your search:",
#             "apartments": [ <parsed list — keep all fields> ],
#             "buttons": null
#           }}

#         If the tool returns an error or empty array return:
#           {{
#             "type": "text",
#             "message": "Sorry, no listings were found for your search.",
#             "apartments": null,
#             "buttons": null
#           }}

#         Your ENTIRE response must be a single valid JSON object — no prose outside it.
#         """,
#         expected_output=(
#             "A single JSON object with type='apartments', a message string, "
#             "an apartments list, and buttons=null."
#         ),
#         output_json=ChatbotResponse,
#         agent=agent,
#     )


# def create_route_task(agent):
#     return Task(
#         description="""
#         The tenant needs to be directed to the correct page on the platform.
#         Read the user_question and pick exactly one of the two routes below.

#         User question : {user_question}

#         ── ROUTE SELECTION ─────────────────────────────────────────────────────

#         IF the question is about eligibility, qualifying for rent, rental budget,
#         or affordability → return:
#           {{
#             "type": "route",
#             "message": "You can check your rental eligibility using our calculator.",
#             "apartments": null,
#             "buttons": [ {{"label": "Open Eligibility Calculator", "route": "calculator"}} ]
#           }}

#         IF the question is about analyzing, reviewing, uploading, or understanding
#         a lease document → return:
#           {{
#             "type": "route",
#             "message": "You can review and analyze your lease using our Lease Analyzer.",
#             "apartments": null,
#             "buttons": [ {{"label": "Open Lease Analyzer", "route": "analysis-upload"}} ]
#           }}

#         Your ENTIRE response must be a single valid JSON object — no prose outside it.
#         """,
#         expected_output=(
#             "A single JSON object with type='route', a message string, apartments=null, "
#             "and a buttons list with exactly one button pointing to the correct page."
#         ),
#         output_json=ChatbotResponse,
#         agent=agent,
#     )


# def create_general_qa_task(agent):
#     return Task(
#         description="""
#         Answer the tenant's general leasing question.

#         Tenant name          : {tenant_name}
#         User question        : {user_question}
#         Session context      : {session_context}
#         Conversation history : {conversation_history}

#         Answer in 2-4 warm, practical sentences. Use session_context if relevant.

#         Return exactly:
#           {{
#             "type": "text",
#             "message": "<your answer here>",
#             "apartments": null,
#             "buttons": null
#           }}

#         Your ENTIRE response must be a single valid JSON object — no prose outside it.
#         """,
#         expected_output=(
#             "A single JSON object with type='text', a message string containing "
#             "the answer, apartments=null, and buttons=null."
#         ),
#         output_json=ChatbotResponse,
#         agent=agent,
#     )


def create_chatbot_manager_task():
    return Task(
        description="""
        A tenant has sent a message. Determine their intent and delegate to the
        correct specialist, then return the specialist's JSON response verbatim.

        Tenant name          : {tenant_name}
        User question        : {user_question}
        Session context      : {session_context}
        Conversation history : {conversation_history}

        ── ROUTING RULES ───────────────────────────────────────────────────────

        PATH 1 — APARTMENT SEARCH → type must be "apartments"
          Trigger : user asks to find, list, or show apartments / residences /
                    rentals in a city, optionally mentioning a price or budget.
          Delegate to: Apartment Search Specialist
          The specialist calls ListingSearchTool which returns a JSON array of
          apartment objects (formatted_address, price, bedrooms, bathrooms, sqft).
          The final response must place that array in the "apartments" field.

        PATH 2 — ELIGIBILITY OR LEASE ROUTING → type must be "route"
          Trigger : user asks about eligibility, qualifying for rent, rental budget,
                    OR asks about analyzing / reviewing / uploading a lease document / lease red flags.
          Delegate to: Navigation Router

        PATH 3 — GENERAL QUESTION → type must be "text"
          Trigger : anything else (tenant rights, deposits, notices, etc.).
          Delegate to: Leasing Q&A Specialist

        ── RULES ───────────────────────────────────────────────────────────────
        • Delegate once to exactly one specialist.
        • Pass tenant_name, user_question, session_context, and
          conversation_history as context when delegating.
        • Your ENTIRE final response must be the specialist's JSON object —
          no prose outside it.
        • route buttons returned by the Navigation Router must have a label and route and put in the buttons attribute.
        """,
        expected_output=(
            "A single JSON object with keys: type (string), message (string), "
            "apartments (list or null), buttons (list or null). No text outside the JSON."
        ),
        output_json=ChatbotResponse,
    )

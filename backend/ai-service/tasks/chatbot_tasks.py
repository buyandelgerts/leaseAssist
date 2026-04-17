# tasks/chatbot_tasks.py
from crewai import Task

def create_chatbot_task(agent):
    return Task(
        description="""
        A tenant has a question and needs a helpful, accurate answer.

        Tenant question: {user_question}
        Tenant name (if known): {tenant_name}
        Previous context (if any): {conversation_history}

        Your job:
        1. Search the LeasingKnowledgeBaseTool for relevant information
        2. Answer the question clearly and concisely (2–4 sentences ideal)
        3. If the question is about a specific lease clause or legal matter, note it
           requires professional legal advice
        4. If you cannot find the answer, direct them to the leasing office contact
        5. End with a follow-up question or offer to help further
        """,
        expected_output="""
        A helpful response containing:
        - Direct answer to the question
        - Source or basis for the answer
        - Contact info if escalation needed
        - Friendly closing
        """,
        agent=agent
    )
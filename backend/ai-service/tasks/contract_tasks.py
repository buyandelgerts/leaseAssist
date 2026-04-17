from crewai import Task

def create_contract_task(agent):
    return Task(
        description="""
        A tenant wants to review their lease agreement before signing.

        Contract details:
        - State where property is located: {state}
        - Contract text: {contract_text}

        Your job:
        1. Use StateLawTool to load the relevant state tenant laws
        2. Use ContractAnalyzerTool to scan the contract
        3. List ALL red flags with severity (CRITICAL / HIGH / MEDIUM)
        4. List ALL green flags that protect the tenant
        5. Give an overall recommendation: SAFE TO SIGN / REVIEW WITH ATTORNEY / DO NOT SIGN
        """,
        expected_output="""
        Contract analysis report with:
        - All red flags with severity and legal citation
        - All green flags with explanation
        - Overall signing recommendation
        - Top 2 negotiation points if red flags exist
        """,
        agent=agent,
        human_input=True,  # HITL: pause for human review before finalizing
        output_file="outputs/contract_analysis.txt"
    )
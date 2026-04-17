# tools/state_law_tool.py
from crewai.tools import tool

@tool("StateLawTool")
def state_law_tool(state: str, topic: str = "general") -> str:
    """
    Returns the key tenant protection laws for a given US state and topic.

    Args:
        state: US state abbreviation (e.g. 'CA', 'TX', 'NY')
        topic: Law topic: 'deposit', 'entry', 'eviction', 'habitability', 'general'
    """
    from tools.contract_analyzer_tool import STATE_LAWS
    state = state.upper()
    laws = STATE_LAWS.get(state)
    if not laws:
        return f"State '{state}' not in database. Supported: CA, TX, NY, FL."

    if topic == "deposit":
        return f"{state} Security Deposit: {laws['max_security_deposit']}"
    elif topic == "entry":
        return f"{state} Notice to Enter: {laws['notice_to_enter']}"
    elif topic == "habitability":
        return f"{state} Habitability: {laws['habitability']}"
    else:
        return f"""
{state} Key Tenant Laws:
  Security deposit : {laws['max_security_deposit']}
  Entry notice     : {laws['notice_to_enter']}
  Rent increase    : {laws['rent_increase_notice']}
  Habitability     : {laws['habitability']}
  Watch for        : {', '.join(laws['illegal_clauses'])}
"""
# tools/property_filter_tool.py
from crewai.tools import tool

@tool("PropertyFilterTool")
def property_filter_tool(property_id: str) -> str:
    """
    Returns full details and availability status for a specific property by ID.

    Args:
        property_id: The property ID (e.g. 'P001')
    """
    from tools.property_search_tool import PROPERTY_DB
    for p in PROPERTY_DB:
        if p["id"] == property_id:
            return str(p)
    return f"Property {property_id} not found."
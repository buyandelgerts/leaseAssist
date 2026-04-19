import os
import smtplib
from email.mime.text import MIMEText

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

from tools.contract_analyzer_tool import STATE_LAWS
from tools.leasing_kb_tool import LEASING_FAQ
from tools.property_search_tool import PROPERTY_DB

mcp = FastMCP("LeaseAssist AI Tools")

API_SERVICE_URL = os.getenv("API_SERVICE_URL", "http://localhost:8001")


@mcp.tool()
def calculate_rental_eligibility(
    monthly_income: float,
    monthly_debts: float,
    state: str,
) -> str:
    """
    Calculate rental affordability using the 30% income rule and DTI ratio.
    Returns ELIGIBLE / BORDERLINE / NOT ELIGIBLE verdict with safe budget range.

    Args:
        monthly_income: Gross monthly income in USD
        monthly_debts: Total monthly debt payments
        state: US state abbreviation (e.g. 'CA', 'TX')
    """
    max_rent_30pct = monthly_income * 0.30
    max_rent_dti = max(0, (monthly_income * 0.43) - monthly_debts)
    safe_budget = min(max_rent_30pct, max_rent_dti)

    state_multipliers = {
        "CA": 2.5, "NY": 3.0, "TX": 2.5, "FL": 2.5,
        "WA": 2.5, "IL": 2.5, "MA": 3.0, "default": 2.5,
    }
    multiplier = state_multipliers.get(state.upper(), state_multipliers["default"])
    max_rent_income_req = monthly_income / multiplier
    final_budget = min(safe_budget, max_rent_income_req)

    dti_ratio = (monthly_debts / monthly_income) * 100 if monthly_income > 0 else 100
    if dti_ratio > 50:
        verdict = "NOT ELIGIBLE"
        reason = f"Debt-to-income ratio is {dti_ratio:.1f}% — too high (max 43%)"
    elif final_budget < 600:
        verdict = "NOT ELIGIBLE"
        reason = "Affordable budget is below minimum rental threshold"
    elif dti_ratio > 35:
        verdict = "BORDERLINE"
        reason = f"DTI is {dti_ratio:.1f}%. Manageable but tight. Guarantor recommended."
    else:
        verdict = "ELIGIBLE"
        reason = f"Income and debt levels meet {state.upper()} rental standards"

    return f"""
=== ELIGIBILITY REPORT ===
Verdict: {verdict}
Reason: {reason}

Income Details:
  Monthly gross income: ${monthly_income:,.2f}
  Monthly debts: ${monthly_debts:,.2f}
  Debt-to-income ratio: {dti_ratio:.1f}%

Affordability:
  Max rent (30% rule): ${max_rent_30pct:,.2f}
  Max rent (DTI rule): ${max_rent_dti:,.2f}
  Max rent ({state} income req {multiplier}x): ${max_rent_income_req:,.2f}
  SAFE BUDGET RANGE: $600 – ${final_budget:,.2f}/month

State: {state.upper()}
"""


@mcp.tool()
def analyze_lease_contract(contract_text: str, state: str) -> str:
    """
    Analyze a lease contract for red and green flags based on state law.

    Args:
        contract_text: Full text of the lease contract
        state: US state abbreviation (e.g. 'CA', 'TX', 'NY', 'FL')
    """
    state = state.upper()
    laws = STATE_LAWS.get(state, STATE_LAWS["TX"])
    contract_lower = contract_text.lower()

    red_flags = []
    green_flags = []

    if "security deposit" in contract_lower:
        if state == "CA" and "three months" in contract_lower:
            red_flags.append({
                "clause": "Security deposit exceeds legal limit",
                "detail": f"CA law: {laws['max_security_deposit']}",
                "severity": "HIGH",
            })
        elif "non-refundable deposit" in contract_lower:
            red_flags.append({
                "clause": "Non-refundable deposit clause found",
                "detail": "Deposits are generally refundable under state law",
                "severity": "HIGH",
            })

    if any(p in contract_lower for p in ["enter at any time", "without notice", "right to enter without"]):
        red_flags.append({
            "clause": "Landlord entry without notice",
            "detail": f"{state} law requires: {laws['notice_to_enter']}",
            "severity": "HIGH",
        })

    if "waive" in contract_lower and "right" in contract_lower:
        red_flags.append({
            "clause": "Tenant rights waiver detected",
            "detail": "Tenants cannot legally waive statutory rights in most states",
            "severity": "HIGH",
        })

    if "automatically renew" in contract_lower and "notice" not in contract_lower:
        red_flags.append({
            "clause": "Automatic renewal without notice provision",
            "detail": "Lease auto-renews with no notice requirement — unfavorable to tenant",
            "severity": "MEDIUM",
        })

    if any(p in contract_lower for p in ["change locks", "remove belongings without", "lockout"]):
        red_flags.append({
            "clause": "Self-help eviction language",
            "detail": "Self-help eviction is illegal in all 50 states",
            "severity": "CRITICAL",
        })

    if "landlord may change" in contract_lower or "modify terms at any time" in contract_lower:
        red_flags.append({
            "clause": "Landlord can modify lease unilaterally",
            "detail": "Contract terms cannot be changed without mutual written consent",
            "severity": "HIGH",
        })

    if any(p in contract_lower for p in ["24 hours notice", "24-hour notice", "advance notice"]):
        green_flags.append({
            "clause": "Proper entry notice provision",
            "detail": f"Aligns with {state} law: {laws['notice_to_enter']}",
        })

    if "return" in contract_lower and "deposit" in contract_lower:
        green_flags.append({
            "clause": "Security deposit return clause present",
            "detail": f"{state} requirement: {laws['max_security_deposit']}",
        })

    if "landlord shall maintain" in contract_lower or "landlord responsible for repairs" in contract_lower:
        green_flags.append({
            "clause": "Landlord maintenance responsibility stated",
            "detail": f"Consistent with {state} habitability law: {laws['habitability']}",
        })

    if "grace period" in contract_lower:
        green_flags.append({
            "clause": "Late payment grace period included",
            "detail": "Gives tenant buffer before late fees apply — tenant-friendly",
        })

    if "written notice" in contract_lower and "rent increase" in contract_lower:
        green_flags.append({
            "clause": "Written rent increase notice required",
            "detail": f"{state} requirement: {laws['rent_increase_notice']}",
        })

    output = f"\n=== CONTRACT ANALYSIS REPORT — {state} ===\n"
    output += f"State law applied: {state}\n"
    output += f"Total flags found: {len(red_flags)} red, {len(green_flags)} green\n"

    output += "\n🔴 RED FLAGS (Review before signing):\n"
    if red_flags:
        for i, flag in enumerate(red_flags, 1):
            output += f"  {i}. [{flag['severity']}] {flag['clause']}\n     → {flag['detail']}\n"
    else:
        output += "  None detected.\n"

    output += "\n🟢 GREEN FLAGS (Tenant-favorable):\n"
    if green_flags:
        for i, flag in enumerate(green_flags, 1):
            output += f"  {i}. {flag['clause']}\n     → {flag['detail']}\n"
    else:
        output += "  None detected.\n"

    output += "\n⚠️ NOTE: This is an automated analysis, not legal advice.\n"
    output += "     Consult a licensed attorney for binding legal interpretation.\n"
    return output


@mcp.tool()
def get_state_law(state: str, topic: str = "general") -> str:
    """
    Returns key tenant protection laws for a given US state and topic.

    Args:
        state: US state abbreviation (e.g. 'CA', 'TX', 'NY')
        topic: Law topic — 'deposit', 'entry', 'habitability', or 'general'
    """
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


@mcp.tool()
def search_properties(
    city: str,
    max_budget: float,
    min_beds: int = 1,
    pet_friendly: bool | None = None,
) -> str:
    """
    Search available properties by city, budget, and bedroom count.
    Returns top 3 ranked matches.

    Args:
        city: Target city name (e.g. 'Austin', 'Los Angeles')
        max_budget: Maximum monthly rent in USD
        min_beds: Minimum number of bedrooms needed
        pet_friendly: True if tenant has pets
    """
    results = []
    for p in PROPERTY_DB:
        if not p["available"]:
            continue
        if p["city"].lower() != city.lower():
            continue
        if p["rent"] > max_budget:
            continue
        if p["beds"] < min_beds:
            continue
        if pet_friendly and not p["pet_friendly"]:
            continue
        budget_score = max(0, 40 * (1 - (p["rent"] / max_budget)))
        bed_score = 30 if p["beds"] == min_beds else 20
        amenity_score = min(30, len(p["amenities"]) * 6)
        results.append({**p, "match_score": round(budget_score + bed_score + amenity_score)})

    if not results:
        return f"No available properties found in {city} within ${max_budget}/month with {min_beds}+ beds."

    results.sort(key=lambda x: x["match_score"], reverse=True)
    output = f"=== TOP {len(results[:3])} PROPERTIES IN {city.upper()} ===\n"
    for i, p in enumerate(results[:3], 1):
        output += f"""
Match #{i} — Score: {p['match_score']}/100
  Address    : {p['address']}, {p['city']}, {p['state']}
  Rent       : ${p['rent']:,}/month
  Size       : {p['beds']} bed / {p['baths']} bath — {p['sqft']} sqft
  Amenities  : {', '.join(p['amenities'])}
  Pet-friendly: {'Yes' if p['pet_friendly'] else 'No'}
  Lease term : {p['lease_term']} months
  Property ID: {p['id']}
"""
    return output


@mcp.tool()
def get_property_details(property_id: str) -> str:
    """
    Get full details for a specific property by ID.

    Args:
        property_id: The property ID (e.g. 'P001')
    """
    for p in PROPERTY_DB:
        if p["id"] == property_id:
            return str(p)
    return f"Property {property_id} not found."


@mcp.tool()
def search_listings(
    query: str,
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
) -> str:
    """
    Search real rental listings from the database.

    Args:
        query: Natural language description of what you're looking for
        city: City to search in (e.g. 'Austin')
        state: State abbreviation (e.g. 'TX')
        max_price: Maximum monthly rent in USD
        min_bedrooms: Minimum number of bedrooms
    """
    payload: dict = {"query": query, "limit": 5}
    if city:
        payload["city"] = city
    if state:
        payload["state"] = state
    if max_price is not None:
        payload["max_price"] = max_price
    if min_bedrooms is not None:
        payload["min_bedrooms"] = min_bedrooms

    try:
        response = httpx.post(f"{API_SERVICE_URL}/search", json=payload, timeout=10.0)
        response.raise_for_status()
        results = response.json().get("results", [])
        if not results:
            return "No listings found in the database matching your criteria."
        lines = [
            f"• {r.get('formatted_address', 'N/A')} — "
            f"${r.get('price', '?')}/mo, "
            f"{r.get('bedrooms', '?')}bd/{r.get('bathrooms', '?')}ba, "
            f"{r.get('sqft', 'N/A')} sqft"
            for r in results
        ]
        return "\n".join(lines)
    except httpx.ConnectError:
        return "Listing database is currently unavailable. Please try again later."
    except Exception as e:
        return f"Could not retrieve listings: {str(e)}"


@mcp.tool()
def lookup_leasing_faq(question: str) -> str:
    """
    Search the leasing knowledge base to answer tenant questions.

    Args:
        question: The tenant's question as a string
    """
    question_lower = question.lower()

    for key, answer in LEASING_FAQ.items():
        if any(word in question_lower for word in key.split()):
            return f"[Source: Leasing Knowledge Base — '{key}']\n{answer}"

    best_match, best_score = None, 0
    for key, answer in LEASING_FAQ.items():
        score = sum(1 for kw in key.split() if kw in question_lower)
        if score > best_score:
            best_score, best_match = score, answer

    if best_match:
        return f"[Source: Best match from Knowledge Base]\n{best_match}"

    return (
        "I don't have a specific answer for that question in my knowledge base. "
        "Please contact our leasing office directly:\n"
        "Email: leasing@yourproperty.com | Phone: (555) 123-4567"
    )


@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email to the specified recipient via Gmail SMTP.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Full email body text
    """
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = to
    msg["From"] = sender
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return f"Email successfully sent to {to}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


# Expose as ASGI app:  uvicorn mcp_server:app --port 8003
app = mcp.sse_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
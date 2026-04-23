import json
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

from db.vector_store import similarity_search
from tools.contract_analyzer_tool import STATE_LAWS
from tools.leasing_kb_tool import LEASING_FAQ

mcp = FastMCP("LeaseAssist AI Tools")


def _is_valid_email(email: str) -> bool:
    _, parsed = parseaddr(email or "")
    return "@" in parsed and "." in parsed.split("@")[-1]


def _send_gmail_email(to: str, subject: str, body: str) -> str:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["To"] = to
    msg["From"] = sender
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
    return f"Email successfully sent to {to}"


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
def search_listings_json(
    query: str,
    city: str,
    state: str,
    max_budget: int | None = None,
    limit: int = 3,
) -> str:
    """
    Search real rental listings and return structured JSON for apartment cards.
    Use this when the user asks about apartments or residences in a specific city.
    Calls the database directly and returns a JSON array of apartment objects.

    Args:
        query: Natural language description (e.g. "2-bedroom apartment around $1800")
        city: City name (e.g. "Austin")
        state: 2-letter state abbreviation (e.g. "TX")
        max_budget: Maximum monthly rent in USD
        limit: Maximum number of results to return (default 3)
    """
    try:
        results = similarity_search(
            query=query or None,
            city=city,
            state=state,
            limit=limit,
        )
        if not results:
            return json.dumps([])
        return json.dumps(results)
    except Exception as e:
        return json.dumps({"error": f"Could not retrieve listings: {str(e)}"})


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
    try:
        return _send_gmail_email(to=to, subject=subject, body=body)
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@mcp.tool()
def send_apartment_tour_request(
    landlord_email: str,
    tenant_name: str,
    property_address: str,
    preferred_date: str,
    preferred_time: str,
    tenant_phone: str | None = None,
    message: str | None = None,
) -> str:
    """
    Send a pre-formatted apartment tour request email to a landlord.

    Args:
        landlord_email: Landlord/leasing contact email
        tenant_name: Name of the prospective tenant
        property_address: Property address the tenant wants to tour
        preferred_date: Preferred tour date (e.g. 'May 3, 2026')
        preferred_time: Preferred time window (e.g. '5:30 PM' or '5-6 PM')
        tenant_phone: Optional tenant phone for landlord follow-up
        message: Optional additional message for landlord
    """
    if not _is_valid_email(landlord_email):
        return "Failed to send email: invalid landlord_email format."

    subject = f"Apartment Tour Request - {property_address}"

    contact_lines = []
    if tenant_phone:
        contact_lines.append(f"- Phone: {tenant_phone}")
    contact_block = "\n".join(contact_lines) if contact_lines else "- Preferred contact: reply to this email"

    extra_message = f"\nAdditional note:\n{message.strip()}\n" if message and message.strip() else ""

    body = (
        f"Hello,\n\n"
        f"My name is {tenant_name}, and I am interested in touring the apartment at:\n"
        f"{property_address}\n\n"
        f"I would like to request a tour on {preferred_date} at {preferred_time}.\n"
        f"If that slot is unavailable, I would appreciate alternative options.\n"
        f"{extra_message}\n"
        f"My contact details:\n"
        f"{contact_block}\n\n"
        f"Thank you for your time,\n"
        f"{tenant_name}\n"
    )

    try:
        return _send_gmail_email(to=landlord_email, subject=subject, body=body)
    except Exception as e:
        return f"Failed to send email: {str(e)}"


# Expose as ASGI app:  uvicorn mcp_server:app --port 8003
app = mcp.sse_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
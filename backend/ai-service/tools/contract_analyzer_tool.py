# tools/contract_analyzer_tool.py
from crewai.tools import tool

# State-specific red flag clauses and laws
STATE_LAWS = {
    "CA": {
        "max_security_deposit": "2 months rent (unfurnished) — CA Civil Code 1950.5",
        "notice_to_enter": "24 hours written notice required — CA Civil Code 1954",
        "rent_increase_notice": "90 days for increases over 10% — CA Civil Code 827",
        "habitability": "Landlord must maintain habitable conditions — Green v. Superior Court",
        "illegal_clauses": ["waiver of habitability", "automatic renewal without notice", "entry without notice"],
    },
    "TX": {
        "max_security_deposit": "No statutory limit, but must be returned in 30 days",
        "notice_to_enter": "No statute requires notice, but 24 hrs is standard practice",
        "rent_increase_notice": "30 days notice required for month-to-month",
        "habitability": "Landlord duty to repair — TX Property Code 92.052",
        "illegal_clauses": ["waiver of repair rights", "no notice eviction", "mandatory arbitration"],
    },
    "NY": {
        "max_security_deposit": "1 month rent (regulated) — NY Real Property Law 227-e",
        "notice_to_enter": "Reasonable notice required, 24 hrs standard",
        "rent_increase_notice": "30–90 days depending on tenancy length — NY RPL 226-c",
        "habitability": "Warranty of habitability — NY Real Property Law 235-b",
        "illegal_clauses": ["waiver of habitability warranty", "excessive late fees", "no pets clauses for service animals"],
    },
    "FL": {
        "max_security_deposit": "No limit, must return within 15–60 days — FL Statute 83.49",
        "notice_to_enter": "12 hours notice required — FL Statute 83.53",
        "rent_increase_notice": "15 days for month-to-month — FL Statute 83.57",
        "habitability": "Landlord must maintain premises — FL Statute 83.51",
        "illegal_clauses": ["self-help eviction", "waiver of notice", "unilateral lease changes"],
    },
}

@tool("ContractAnalyzerTool")
def contract_analyzer_tool(contract_text: str, state: str) -> str:
    """
    Analyzes a lease contract for red flags and green flags
    based on the laws of the specified US state.

    Args:
        contract_text: The full text of the lease contract
        state: US state abbreviation (e.g. 'CA', 'TX', 'NY', 'FL')
    """
    state = state.upper()
    laws = STATE_LAWS.get(state, STATE_LAWS["TX"])  # Default to TX if unknown
    contract_lower = contract_text.lower()

    red_flags = []
    green_flags = []

    # ---- RED FLAG CHECKS ----

    # 1. Security deposit
    if "security deposit" in contract_lower:
        if state == "CA" and "three months" in contract_lower:
            red_flags.append({
                "clause": "Security deposit exceeds legal limit",
                "detail": f"CA law: {laws['max_security_deposit']}",
                "severity": "HIGH"
            })
        elif "non-refundable deposit" in contract_lower:
            red_flags.append({
                "clause": "Non-refundable deposit clause found",
                "detail": "Deposits are generally refundable under state law",
                "severity": "HIGH"
            })

    # 2. Entry without notice
    if any(phrase in contract_lower for phrase in [
        "enter at any time", "without notice", "right to enter without"
    ]):
        red_flags.append({
            "clause": "Landlord entry without notice",
            "detail": f"{state} law requires: {laws['notice_to_enter']}",
            "severity": "HIGH"
        })

    # 3. Waiver of rights
    if "waive" in contract_lower and "right" in contract_lower:
        red_flags.append({
            "clause": "Tenant rights waiver detected",
            "detail": "Tenants cannot legally waive statutory rights in most states",
            "severity": "HIGH"
        })

    # 4. Automatic renewal trap
    if "automatically renew" in contract_lower and "notice" not in contract_lower:
        red_flags.append({
            "clause": "Automatic renewal without notice provision",
            "detail": "Lease auto-renews with no notice requirement — unfavorable to tenant",
            "severity": "MEDIUM"
        })

    # 5. Illegal self-help eviction
    if any(phrase in contract_lower for phrase in [
        "change locks", "remove belongings without", "lockout"
    ]):
        red_flags.append({
            "clause": "Self-help eviction language",
            "detail": "Self-help eviction is illegal in all 50 states",
            "severity": "CRITICAL"
        })

    # 6. Unilateral modification
    if "landlord may change" in contract_lower or "modify terms at any time" in contract_lower:
        red_flags.append({
            "clause": "Landlord can modify lease unilaterally",
            "detail": "Contract terms cannot be changed without mutual written consent",
            "severity": "HIGH"
        })

    # ---- GREEN FLAG CHECKS ----

    # 1. Notice to enter
    if any(phrase in contract_lower for phrase in [
        "24 hours notice", "24-hour notice", "advance notice"
    ]):
        green_flags.append({
            "clause": "Proper entry notice provision",
            "detail": f"Aligns with {state} law: {laws['notice_to_enter']}"
        })

    # 2. Security deposit return timeline
    if "return" in contract_lower and "deposit" in contract_lower:
        green_flags.append({
            "clause": "Security deposit return clause present",
            "detail": f"{state} requirement: {laws['max_security_deposit']}"
        })

    # 3. Repair and maintenance
    if "landlord shall maintain" in contract_lower or "landlord responsible for repairs" in contract_lower:
        green_flags.append({
            "clause": "Landlord maintenance responsibility stated",
            "detail": f"Consistent with {state} habitability law: {laws['habitability']}"
        })

    # 4. Grace period for late payments
    if "grace period" in contract_lower:
        green_flags.append({
            "clause": "Late payment grace period included",
            "detail": "Gives tenant buffer before late fees apply — tenant-friendly"
        })

    # 5. Written notice for rent increase
    if "written notice" in contract_lower and "rent increase" in contract_lower:
        green_flags.append({
            "clause": "Written rent increase notice required",
            "detail": f"{state} requirement: {laws['rent_increase_notice']}"
        })

    # Build output
    output = f"\n=== CONTRACT ANALYSIS REPORT — {state} ===\n"
    output += f"State law applied: {state}\n"
    output += f"Total flags found: {len(red_flags)} red, {len(green_flags)} green\n"

    output += "\n🔴 RED FLAGS (Review before signing):\n"
    if red_flags:
        for i, flag in enumerate(red_flags, 1):
            output += f"  {i}. [{flag['severity']}] {flag['clause']}\n"
            output += f"     → {flag['detail']}\n"
    else:
        output += "  None detected.\n"

    output += "\n🟢 GREEN FLAGS (Tenant-favorable):\n"
    if green_flags:
        for i, flag in enumerate(green_flags, 1):
            output += f"  {i}. {flag['clause']}\n"
            output += f"     → {flag['detail']}\n"
    else:
        output += "  None detected.\n"

    output += "\n⚠️ NOTE: This is an automated analysis, not legal advice.\n"
    output += "     Consult a licensed attorney for binding legal interpretation.\n"
    return output
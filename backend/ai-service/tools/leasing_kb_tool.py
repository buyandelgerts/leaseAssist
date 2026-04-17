# tools/leasing_kb_tool.py
from crewai.tools import tool

# This is your knowledge base. In production, back this with a vector DB.
LEASING_FAQ = {
    "application process": """
The typical rental application process:
1. Browse listings and schedule a viewing
2. Submit application: ID, pay stubs, references, credit consent
3. Landlord runs background/credit check (3–5 business days)
4. Receive approval or denial with reason
5. Pay security deposit and first month's rent to secure unit
6. Sign lease agreement — both parties must sign
7. Get keys and move-in inspection checklist
""",
    "security deposit": """
A security deposit is money paid upfront to cover potential damages.
- Typically 1–2 months rent depending on state
- Must be returned within 14–60 days after move-out (varies by state)
- Landlord must provide itemized deduction list if keeping any portion
- Normal wear and tear cannot be deducted
""",
    "lease termination": """
How to terminate a lease early:
- Review your lease for early termination clause
- Give written notice (30–60 days typical)
- You may owe an early termination fee (1–2 months rent)
- Military deployment: SCRA protection allows penalty-free termination
- Domestic violence: Many states allow lease break without penalty
- Landlord breach: If landlord fails duties, you may break lease legally
""",
    "tenant rights": """
Core tenant rights in the US:
- Right to habitable living conditions (heat, water, no pests)
- Right to privacy (landlord must give notice before entering)
- Right to security deposit return with itemized deductions
- Right to 30-day notice before eviction proceedings
- Right to not be discriminated against (Fair Housing Act)
- Right to repair-and-deduct in many states if landlord won't fix issues
""",
    "pet policy": """
Pet policies vary by property:
- Some buildings are fully pet-free (no exceptions except service animals)
- Pet-friendly buildings may charge a pet deposit (refundable) or pet fee (non-refundable)
- Monthly pet rent ($25–$100) is also common
- Service animals and emotional support animals have special legal protections
- Always get pet approval in writing before signing
""",
    "late rent": """
What happens if rent is late:
- Most leases have a 3–5 day grace period before late fees apply
- Late fees typically range from $25 to 5–10% of monthly rent
- After ~5–7 days: landlord may issue Pay or Quit notice
- After notice period: eviction proceedings can begin
- Communicate early with your landlord if you're struggling — many will work with you
""",
    "contact": """
Leasing office contact:
- Email: leasing@yourproperty.com
- Phone: (555) 123-4567
- Hours: Monday–Friday 9am–6pm, Saturday 10am–4pm
- Emergency maintenance: (555) 999-0000 (24/7)
- Online portal: https://portal.yourproperty.com
""",
}

@tool("LeasingKnowledgeBaseTool")
def leasing_kb_tool(question: str) -> str:
    """
    Searches the leasing knowledge base to answer tenant questions
    about applications, deposits, rights, policies, and contacts.

    Args:
        question: The tenant's question as a string
    """
    question_lower = question.lower()

    # Keyword matching — in production, replace with semantic search / RAG
    best_match = None
    best_score = 0
    for key, answer in LEASING_FAQ.items():
        keywords = key.split()
        score = sum(1 for kw in keywords if kw in question_lower)
        if score > best_score:
            best_score = score
            best_match = answer

    # Also do direct phrase matching
    for key, answer in LEASING_FAQ.items():
        if any(word in question_lower for word in key.split()):
            return f"[Source: Leasing Knowledge Base — '{key}']\n{answer}"

    if best_match:
        return f"[Source: Best match from Knowledge Base]\n{best_match}"

    return (
        "I don't have a specific answer for that question in my knowledge base. "
        "Please contact our leasing office directly:\n"
        "Email: leasing@yourproperty.com | Phone: (555) 123-4567"
    )
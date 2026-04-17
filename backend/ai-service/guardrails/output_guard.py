# guardrails/output_guard.py
import re

def validate_eligibility_output(output: str) -> str:
    """Ensures eligibility output contains a clear verdict."""
    required_keywords = ["ELIGIBLE", "NOT ELIGIBLE", "BORDERLINE"]
    if not any(kw in output.upper() for kw in required_keywords):
        raise ValueError("Output guardrail: eligibility verdict missing from response")
    # Redact any accidentally included SSN patterns
    output = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', output)
    return output

def validate_contract_output(output: str) -> str:
    """Ensures contract output includes a signing recommendation."""
    required = ["SAFE TO SIGN", "REVIEW WITH ATTORNEY", "DO NOT SIGN"]
    if not any(r in output.upper() for r in required):
        raise ValueError("Output guardrail: contract recommendation missing")
    return output

def validate_chatbot_output(output: str) -> str:
    """Ensures chatbot doesn't hallucinate legal advice."""
    legal_advice_phrases = [
        "you should sue", "you will win", "this is illegal and you can",
        "i guarantee", "100% certain"
    ]
    for phrase in legal_advice_phrases:
        if phrase in output.lower():
            return output.replace(phrase, "[Note: consult a licensed attorney for legal advice]")
    return output
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

def validate_lease_analyzer_output(output: str) -> str:
    """Ensures lease analyzer output includes red/green flag assessments."""
    upper = output.upper()
    if "RED" not in upper and "GREEN" not in upper:
        raise ValueError("Output guardrail: lease analysis must include RED or GREEN flag assessments")
    return output


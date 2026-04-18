# tasks/lease_analyzer_tasks.py
from crewai import Task
from crewai.tasks.task_output import TaskOutput
from pydantic import BaseModel, Field
from typing import List


# -------------------------
# Structured Output Models
# -------------------------
class ClauseAssessment(BaseModel):
    """Assessment of a single lease clause."""
    clause: str = Field(description="The lease clause being assessed")
    severity: str = Field(description="RED, YELLOW, or GREEN")
    reason: str = Field(description="Why this severity was assigned")
    applicable_law: str = Field(description="Relevant law or standard, or 'N/A' if none")


class LeaseRedFlagReport(BaseModel):
    """Complete red flag report for a lease."""
    city: str = Field(description="City the lease is in")
    total_red_flags: int = Field(description="Number of RED severity clauses")
    total_warnings: int = Field(description="Number of YELLOW severity clauses")
    assessments: List[ClauseAssessment] = Field(description="Assessment for each clause")


class FlagItem(BaseModel):
    """A single red or green flag item for the UI."""
    type: str = Field(description="Either 'red' or 'green'")
    title: str = Field(description="Short title, e.g. 'Security Deposit', 'Monthly Rent'")
    text: str = Field(description="What the lease clause says, e.g. '2-month security deposit required'")
    reason: str = Field(description="For red: why this violates the law or is unfair. For green: why this is acceptable and compliant")
    action: str = Field(description="For red: specific ask to the landlord to fix this. For green: leave empty string")
    section: str = Field(description="For red: the applicable law citation e.g. 'California Civil Code § 1950.5'. For green: 'Compliant'")
    tag: str = Field(description="Short uppercase category label, e.g. 'DEPOSIT', 'RENT', 'PETS', 'ENTRY NOTICE'")


class LeaseAnalysisResult(BaseModel):
    """Final structured output for lease analysis UI."""
    flags: List[FlagItem] = Field(description="List of all red and green flag items")
    email_draft: str = Field(description="Professional email draft to the landlord addressing all red flag items")


# -------------------------
# Task Callback
# -------------------------
def on_task_complete(output: TaskOutput):
    """Called after each task completes. Tracks progress."""
    print("\n" + "=" * 55)
    print(f"  STAGE COMPLETE | Output: {len(output.raw)} characters")
    print("=" * 55 + "\n")


# -------------------------
# Task Creators
# -------------------------
def scrape_task(agent):
    return Task(
        description=(
            "Extract all lease-related information from the provided input.\n\n"
            "Input type: {inputType}\n"
            "Input: {leaseInput}\n\n"
            "Based on the input type:\n"
            "- If 'url': Use the ScrapeWebsiteTool to scrape the web page and extract lease info.\n"
            "- If 'file': Use PDFSearchTool (for PDFs) or FileReadTool (for DOCX/TXT) to read "
            "the uploaded document and extract lease info.\n"
            "- If 'text': The input already contains the lease terms — pass them through directly.\n\n"
            "Extract everything related to:\n"
            "- Rent amount and payment terms\n"
            "- Security deposit\n"
            "- Lease duration\n"
            "- Pet policy\n"
            "- Subletting rules\n"
            "- Move-in/move-out conditions\n"
            "- Landlord entry and notice policies\n"
            "- Any fees, penalties, or restrictions\n"
            "- Property details (address, city, bedrooms, amenities)\n\n"
            "Return ALL lease-related text found."
        ),
        expected_output=(
            "A comprehensive extraction of all lease terms, conditions, fees, "
            "restrictions, and property details from the provided input."
        ),
        agent=agent,
        callback=on_task_complete
    )


def extract_task(agent, scrape_task):
    return Task(
        description=(
            "Parse the scraped apartment listing data and organize the lease terms "
            "into structured categories.\n\n"
            "City: {cityName}\n\n"
            "Organize into these categories:\n"
            "- Rent (monthly amount, due date, late fees)\n"
            "- Security Deposit (amount, conditions for return)\n"
            "- Restrictions (pets, subletting, guests, modifications)\n"
            "- Penalties (early termination, lease breaking fees)\n"
            "- Landlord Rights (entry notice, inspection rules)\n"
            "- Lease Duration and Renewal terms\n"
            "- Any other notable clauses"
        ),
        expected_output=(
            "A well-organized breakdown of all lease clauses sorted by category, "
            "with each term clearly stated."
        ),
        agent=agent,
        context=[scrape_task],
        callback=on_task_complete
    )


def red_flag_task(agent, extract_task):
    return Task(
        description=(
            "Review the structured lease clauses and identify any red flags.\n\n"
            "For the city of {cityName}, check each clause against known tenant protection laws.\n"
            "For each clause, provide:\n"
            "- The clause text\n"
            "- Severity: RED (likely illegal/very unfair), YELLOW (unusual/risky), GREEN (acceptable)\n"
            "- Why it is flagged (legal reason or fairness concern)\n"
            "- The applicable law or standard (or 'N/A')\n\n"
            "You MUST review ALL clauses including: rent, deposit, subletting, "
            "termination, pets, and landlord entry."
        ),
        expected_output=(
            "A structured assessment of each lease clause with severity, reasoning, "
            "and applicable laws."
        ),
        agent=agent,
        context=[extract_task],
        output_pydantic=LeaseRedFlagReport,

        callback=on_task_complete
    )


def compare_task(agent, extract_task, red_flag_task):
    return Task(
        description=(
            "Compare the lease terms against typical market standards for {cityName}.\n\n"
            "For each major term, state:\n"
            "- What this lease offers\n"
            "- What is typical in {cityName}\n"
            "- Verdict: ABOVE MARKET / AT MARKET / BELOW MARKET / NON-STANDARD\n\n"
            "Cover: rent amount, deposit, restrictions, penalties, and landlord access terms."
        ),
        expected_output=(
            "A term-by-term comparison table showing this lease vs. market standard, "
            "with a clear verdict for each."
        ),
        agent=agent,
        context=[extract_task, red_flag_task],
        callback=on_task_complete
    )


def negotiate_task(agent, extract_task, red_flag_task, compare_task):
    return Task(
        description=(
            "Based on all the findings, create a negotiation strategy for the tenant.\n\n"
            "Format your response in THREE clearly separated sections:\n\n"
            "SECTION 1 — RED FLAGS:\n"
            "List each non-compliant or illegal clause as a numbered item.\n"
            "For each item write exactly like this example:\n"
            "1. Security Deposit\n"
            "   The lease requires a 2-month security deposit. California Civil Code § 1950.5 "
            "limits deposits to 2 months for unfurnished units. The conditions for return are "
            "not specified, which is required by law. Request clear deposit return conditions "
            "and confirm compliance with § 1950.5.\n\n"
            "SECTION 2 — GREEN FLAGS:\n"
            "List each compliant clause as a numbered item.\n"
            "For each item write exactly like this example:\n"
            "1. Monthly Rent: $1,800/month\n"
            "   This is within the typical market range and clearly stated.\n\n"
            "SECTION 3 — DRAFT EMAIL:\n"
            "Write a professional email the tenant can send to the landlord requesting "
            "changes for all RED FLAG items. Keep the tone polite but firm. "
            "Do NOT use any markdown formatting — plain text only.\n"
            "The landlord email is: {landlordEmail}\n"
            "Extract the landlord name from the email address (the part before @, "
            "capitalize it properly) and use it in the greeting instead of [Landlord's Name].\n"
            "For example if the email is john.smith@gmail.com, write 'Dear John Smith,'.\n"
            "Also extract the property address from the lease text and use it in the email "
            "instead of [Property Address]. If no address is found, use the city name: {cityName}.\n\n"
            "IMPORTANT RULES:\n"
            "- Do NOT use any markdown (no **, no ##, no ---).\n"
            "- Write in plain text only.\n"
            "- Every lease item must be either RED or GREEN. No middle category.\n"
            "- For red items, always cite the applicable state/city law.\n"
            "- Keep descriptions clear and concise like a professional email."
        ),
        expected_output=(
            "Three sections: RED FLAGS (numbered list with title and description), "
            "GREEN FLAGS (numbered list with title and description), "
            "and DRAFT EMAIL (professional plain-text email to landlord)."
        ),
        agent=agent,
        context=[extract_task, red_flag_task, compare_task],
        callback=on_task_complete
    )



from pydantic import BaseModel, validator, Field
from typing import Optional

class EligibilityInput(BaseModel):
    monthly_income: float = Field(..., gt=0, description="Gross monthly income in USD")
    monthly_debts: float = Field(..., ge=0, description="Total monthly debt payments")
    state: str = Field(..., min_length=2, max_length=2, description="US state abbreviation")
    desired_budget: float = Field(..., gt=0)

    @validator("state")
    def validate_state(cls, v):
        valid_states = [
            "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
            "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
            "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
            "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
            "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
        ]
        if v.upper() not in valid_states:
            raise ValueError(f"'{v}' is not a valid US state abbreviation")
        return v.upper()

    @validator("monthly_income")
    def validate_income(cls, v):
        if v > 1_000_000:
            raise ValueError("Monthly income seems unrealistically high")
        return v

class PropertyInput(BaseModel):
    city: str = Field(..., min_length=2, description="Target city")
    max_budget: float = Field(..., gt=500, description="Max monthly rent")
    min_beds: int = Field(1, ge=1, le=6)
    pet_friendly: Optional[bool] = False
    special_requirements: Optional[str] = ""

class ContractInput(BaseModel):
    state: str = Field(..., min_length=2, max_length=2)
    contract_text: str = Field(..., min_length=100, description="Full contract text")

    @validator("contract_text")
    def validate_contract_length(cls, v):
        if len(v) < 100:
            raise ValueError("Contract text is too short to be a real lease")
        return v

class LeaseAnalyzerInput(BaseModel):
    inputType: str = Field(..., description="Input type: 'text', 'url', or 'file'")
    leaseInput: str = Field(..., min_length=10, description="Lease text, URL, or file path")
    cityName: str = Field(..., min_length=2, description="City name for local law comparison")
    landlordEmail: Optional[str] = "landlord@example.com"

    @validator("inputType")
    def validate_input_type(cls, v):
        if v not in ("text", "url", "file"):
            raise ValueError("inputType must be 'text', 'url', or 'file'")
        return v

class ChatbotInput(BaseModel):
    user_question: str = Field(..., min_length=3, max_length=1000)
    tenant_name: Optional[str] = "Tenant"
    conversation_history: Optional[str] = ""

    @validator("user_question")
    def sanitize_question(cls, v):
        # Block prompt injection attempts
        blocked = ["ignore previous", "system:", "you are now", "jailbreak"]
        if any(phrase in v.lower() for phrase in blocked):
            raise ValueError("Question contains disallowed content")
        return v
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from guardrails.input_guard import (
    EligibilityInput,
    PropertyInput,
    ContractInput,
    ChatbotInput,
    LeaseAnalyzerInput,
)
from guardrails.output_guard import (
    validate_eligibility_output,
    validate_contract_output,
    validate_chatbot_output,
    validate_lease_analyzer_output,
)
from crew import (
    run_eligibility,
    run_property_matcher,
    run_contract_analyzer,
    run_chatbot,
    run_lease_analyzer,
)

load_dotenv()  # loads ai-service/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # loads backend/.env
os.makedirs("outputs", exist_ok=True)

app = FastAPI(
    title="AI Leasing System",
    description="4-process AI leasing assistant powered by crewAI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/eligibility")
async def check_eligibility(data: EligibilityInput):
    try:
        result = run_eligibility(inputs=data.model_dump())
        validated = validate_eligibility_output(str(result))
        return {
            "status": "success",
            "process": "eligibility",
            "result": validated,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/property-match")
async def match_property(data: PropertyInput):
    try:
        result = run_property_matcher(inputs=data.model_dump())
        return {
            "status": "success",
            "process": "property_matcher",
            "result": str(result),
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/analyze-contract")
async def analyze_contract(data: ContractInput):
    try:
        result = run_contract_analyzer(inputs=data.model_dump())
        validated = validate_contract_output(str(result))
        return {
            "status": "success",
            "process": "contract_analyzer",
            "result": validated,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/chat")
async def chat(data: ChatbotInput):
    try:
        result = run_chatbot(inputs=data.model_dump())
        validated = validate_chatbot_output(str(result))
        return {
            "status": "success",
            "process": "chatbot",
            "result": validated,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/analyze-lease")
async def analyze_lease(data: LeaseAnalyzerInput):
    try:
        result = run_lease_analyzer(inputs=data.model_dump())
        return {
            "status": "success",
            "process": "lease_analyzer",
            "result": str(result),
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.get("/")
async def root():
    return {
        "app": "AI Leasing System",
        "version": "1.0.0",
        "endpoints": [
            "/eligibility",
            "/property-match",
            "/analyze-contract",
            "/chat",
            "/analyze-lease",
        ],
    }
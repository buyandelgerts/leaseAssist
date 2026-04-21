import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from crew import run_send_tour_request

from guardrails.input_guard import (
    EligibilityInput,
    ContractInput,
    ChatbotInput,
    LeaseAnalyzerInput,
    SearchInput,
    SessionContext,
    TourRequestInput,
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
    run_search_agent,
    run_eligibility_tasks,
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

@app.get("/")
def root():
    return {"message": "Rental AI Search API is running"}

@app.post("/eligibility")
async def check_eligibility(data: EligibilityInput):
    try:
        result = run_eligibility(inputs=data.model_dump())
        result_text = str(result)
        validated = validate_eligibility_output(result_text)
        try:
            parsed_result = json.loads(validated)
        except json.JSONDecodeError:
            # Fallback shape when agent output is plain text
            parsed_result = {"message": validated}
        return {
            "status": "success",
            "process": "eligibility",
            "result": parsed_result,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


# @app.post("/property-match")
# async def match_property(data: PropertyInput):
#     try:
#         result = run_property_matcher(inputs=data.model_dump())
#         return {
#             "status": "success",
#             "process": "property_matcher",
#             "result": str(result),
#         }
#     except ValueError as e:
#         raise HTTPException(status_code=422, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


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

@app.post("/search")
async def search(data: SearchInput):
    try:
        result = run_search_agent(inputs=data.model_dump())
        return {
            "status": "success",
            "process": "search",
            "result": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.post("/tour-request")
async def send_tour_request(data: TourRequestInput):
    try:
        result = run_send_tour_request(inputs=data.model_dump())
        return {
            "status": "success",
            "process": "tour_request",
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
            "/search",
            "/eligibility-tasks",
            "/tour-request",
        ],
    }
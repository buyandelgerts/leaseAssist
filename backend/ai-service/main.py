import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
        print(f"Raw lease analyzer output===>>:\n{result}\n")
        return {
            "status": "success",
            "process": "lease_analyzer",
            "result": str(result),
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


class RegenerateEmailInput(BaseModel):
    red_flags: list[str]
    landlord_email: str


@app.post("/regenerate-email")
async def regenerate_email(data: RegenerateEmailInput):
    """Regenerate the draft email based on updated red flag list using LLM."""
    from openai import OpenAI
    client = OpenAI()

    red_list = "\n".join(f"- {flag}" for flag in data.red_flags)
    email_parts = data.landlord_email.split("@")[0]
    landlord_name = email_parts.replace(".", " ").replace("_", " ").title()

    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo"),
        messages=[{
            "role": "user",
            "content": (
                f"Write a professional email to the landlord requesting changes for these red flag items:\n\n"
                f"{red_list}\n\n"
                f"Address the email to: Dear {landlord_name},\n"
                f"End with: Best regards,\nGroup 4\n\n"
                f"Keep the tone polite but firm. Plain text only, no markdown."
            )
        }]
    )
    return {
        "status": "success",
        "email_draft": response.choices[0].message.content,
    }


class SendEmailInput(BaseModel):
    to: str
    subject: str
    body: str


@app.post("/send-email")
async def send_email(data: SendEmailInput):
    import smtplib
    from email.mime.text import MIMEText

    sender = os.environ.get("GMAIL_SENDER")
    password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender or not password:
        raise HTTPException(status_code=500, detail="Email credentials not configured")

    msg = MIMEText(data.body)
    msg["Subject"] = data.subject
    msg["To"] = data.to
    msg["From"] = sender

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        return {"status": "success", "message": f"Email sent to {data.to}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


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


# Serve frontend static files in production (Docker/HF Spaces)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse

    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(static_dir, "index.html"))

    @app.get("/{path:path}")
    async def serve_spa(path: str):
        file_path = os.path.join(static_dir, path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
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

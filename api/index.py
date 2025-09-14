from fastapi import FastAPI, Body, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import os
from surge_planner_lib import run_planner

app = FastAPI(title="Surge Planner API (Vercel)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

API_TOKEN = os.getenv("API_TOKEN", "")

def _auth_or_401(auth_header: Optional[str]):
    if not API_TOKEN:
        return
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing/invalid Authorization header")
    if auth_header.split(" ", 1)[1].strip() != API_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

class PlannerOptions(BaseModel):
    cap: float = Field(2.0, ge=1.0, le=5.0)
    ai_events: bool = False
    ai_min_conf: float = Field(0.6, ge=0.0, le=1.0)
    ai_model: str = "openai/gpt-4o-mini"
    days_cover: int = Field(7, ge=1, le=30)
    include_human_brief: bool = False
    nlg_model: str = "openai/gpt-4o-mini"

class PlannerRequest(BaseModel):
    data: Dict[str, Any]
    options: PlannerOptions = PlannerOptions()

@app.get("/healthz")
def healthz():
    return {"ok": True, "runtime": "vercel", "version": "1.0.0"}

@app.post("/v1/surge-plan")
def surge_plan(req: PlannerRequest = Body(...), authorization: Optional[str] = Header(default=None)):
    _auth_or_401(authorization)
    try:
        result = run_planner(
            req.data,
            cap=req.options.cap,
            ai_events=req.options.ai_events,
            ai_min_conf=req.options.ai_min_conf,
            ai_model=req.options.ai_model,
            days_cover=req.options.days_cover,
            include_human_brief=req.options.include_human_brief,
            nlg_model=req.options.nlg_model,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Planner error: {e}")

    notes = {}
    if (req.options.ai_events or req.options.include_human_brief) and not os.getenv("OPENROUTER_API_KEY"):
        notes["warning"] = "OPENROUTER_API_KEY not set; AI features may fallback/skip."
    return {"version": "1.0.0", **result, "notes": notes or None}

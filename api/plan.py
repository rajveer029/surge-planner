# api/plan.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from surge_planner import build_multiplier_plan, apply_multipliers, make_human_nlg
import json

app = FastAPI(title="Surge Planner API")

# CORS (open for testing; lock down origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"ok": True}

@app.post("/plan")
def create_plan(payload: dict):
    plan, features, env_blocks = build_multiplier_plan(
        payload,
        cap=2.0,
        ai_events=True,
        ai_min_conf=0.6,
        ai_model="gpt-4o-mini",
    )
    ts = apply_multipliers(plan, payload.get("baselines", {}))
    translated = json.dumps(ts, indent=2, ensure_ascii=False, sort_keys=True)
    briefing = make_human_nlg(plan, features, env_blocks, translated, model="gpt-4.1-mini")
    return {"translated": translated, "briefing": briefing}

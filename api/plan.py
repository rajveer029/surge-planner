# api/plan.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from surge_planner import build_multiplier_plan, apply_multipliers, make_human_nlg

app = FastAPI()

@app.post("/")
async def create_plan(request: Request):
    payload = await request.json()

    try:
        plan, features, env_blocks = build_multiplier_plan(
            payload,
            cap=2.0,
            ai_events=True,
            ai_min_conf=0.6,
            ai_model="gpt-4o-mini"
        )
        translated = apply_multipliers(plan, payload.get("baselines", {}))
        briefing = make_human_nlg(plan, features, env_blocks, translated, model="gpt-4.1-mini")

        return JSONResponse({
            "translated": translated,
            "briefing": briefing
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

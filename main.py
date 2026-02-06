from fastapi import FastAPI, Header, HTTPException
from datetime import datetime, timezone

from models import HoneypotRequest, HoneypotResponse, ExtractedIntelligence, EngagementMetrics
from agent.agent_loop import run_agent
from mem1.intelligence_store import update_intelligence, build_extracted_intelligence

app = FastAPI()

API_KEY = "secret123"   # move to Render ENV later

@app.get("/")
async def root():
    return {"status": "Honeypot Live", "endpoint": "/honeypot"}

@app.post("/honeypot", response_model=HoneypotResponse)
async def honeypot(req: HoneypotRequest, x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(401, "Invalid API Key")

    conv_id = req.metadata.get("conversation_id", "conv_default")

    ts = datetime.now(timezone.utc).isoformat()

    # --- MEMBER 3 ---
    update_intelligence(conv_id, req.message, "scammer", ts)

    # --- MEMBER 2 ---
    state = {
        "history": [m.dict() for m in req.conversation_history],
        "turn_count": len(req.conversation_history)
    }

    result = run_agent(state, req.message)

    reply = result.get("reply", "")

    update_intelligence(conv_id, reply, "agent", ts)

    intel = build_extracted_intelligence(conv_id)

    metrics = EngagementMetrics(
        total_turns=state["turn_count"],
        scammer_messages=1,
        agent_messages=1
    )

    return HoneypotResponse(
        scam_detected=True,
        confidence_score=0.88,
        agent_response=reply,
        engagement_metrics=metrics,
        extracted_intelligence=ExtractedIntelligence(**intel)
    )

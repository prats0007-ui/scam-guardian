"""The web API. Run: uvicorn server:app --reload --port 8000"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from graph.build import investigate

app = FastAPI(title="Scam Guardian API")

# Lets the website (on port 3000) call this server (on port 8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class CheckRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/check")
def check(req: CheckRequest):
    try:
        result = investigate(req.message)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=502, detail="The investigation didn't finish. Try again in a moment.")
    v = result["verdict"]
    try:
        risk = int(v.get("risk") or 0)
    except (TypeError, ValueError):
        risk = 50
    return {
        "verdict": v["verdict"],
        "risk": risk,
        "scam_type": v.get("scam_type"),
        "reasons": v.get("reasons") or [],
        "sources": v.get("sources") or [],
    }
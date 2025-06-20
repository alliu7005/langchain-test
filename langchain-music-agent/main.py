from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from agent import Query, query_agent
import uvicorn
import os
import json
import urllib
from pydantic import BaseModel

app = FastAPI()

AUTH_SERVER = os.environ.get("AUTH_SERVER", "https://spotify-oauth-365383383851.us-central1.run.app")
AGENT_ID = os.environ.get("AGENT_ID", "music-agent-365383383851")
SPOTIFY_SCOPE = "user-library-read user-top-read"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Location"],
)

class Token(BaseModel):
    token: str

def connect_url(route, prompt):
    scope = SPOTIFY_SCOPE
    config = {"prompt": prompt}
    params = {
        "agent_id": AGENT_ID,
        "scopes": scope,
        "route": route,
        "config": json.dumps(config)
    }
    qs = urllib.parse.urlencode(params)
    return(
        f"{AUTH_SERVER}/login?{qs}"
    )

@app.post("/query")
async def query(query:Query):
    
    if not os.environ.get("TOKEN"):
        # Redirect the user to the login flow if credentials are missing
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ "authUrl": connect_url("query", query.prompt) }
        )
    try:
        resp = query_agent(query)
        return {"status": "success", "message":resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store_credentials")
def store_credentials(token: Token):
    os.environ["TOKEN"] = token.token
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


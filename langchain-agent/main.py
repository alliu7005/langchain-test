from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agent import Query, query_agent
import uvicorn
import os

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/query")
async def query(query:Query):
    response = query_agent(query)
    return {"response": response}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


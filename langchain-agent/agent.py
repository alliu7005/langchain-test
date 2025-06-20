from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://104.155.143.96")
MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")  

llm = Ollama(model=MODEL, base_url=OLLAMA_HOST)

agent = initialize_agent(
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=[],  # you can add your custom tools here
    llm=llm,
    handle_parsing_errors=True,
    verbose=True
)

class Query(BaseModel):
    prompt: str

def query_agent(query:Query):
    response = agent.run(query.prompt)
    return response

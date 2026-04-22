import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from llm_agent import LLMDataAnalystAgent

load_dotenv()

app = FastAPI()

agent = LLMDataAnalystAgent("data/superstore_messy.csv")


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Agentic Data Analyst API is running."}


@app.post("/ask")
def ask_question(request: AskRequest):
    answer = agent.ask(request.question)
    return {"answer": answer}
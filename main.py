from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import run_research_pipeline

app = FastAPI(
    title="AI Research Agent API",
    description="An API that runs an AI agent pipeline to research a given topic, synthesize findings, write a report, and critique it.",
    version="1.0.0",
)


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    search_result: str
    reader_result: str
    writer_result: str
    critic_result: str


@app.post("/api/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest):
    try:
        # The pipeline is synchronous, so we just call it directly.
        # For a truly non-blocking setup in production, this could be run in a background thread or made async.
        state = run_research_pipeline(request.topic)

        return ResearchResponse(
            topic=request.topic,
            search_result=str(state.get("search_result", "")),
            reader_result=str(state.get("reader_result", "")),
            writer_result=str(state.get("writer_result", "")),
            critic_result=str(state.get("critic_result", "")),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# AI Research Agent Backend

This is the backend for the AI Research Agent application. It exposes a FastAPI service that orchestrates a multi-step Langchain agent pipeline to perform deep research on any given topic, write a comprehensive report, and automatically critique that report.

## Tech Stack
- **Framework**: FastAPI (Python)
- **AI / LLM**: LangChain, MistralAI (`mistral-small-latest`)
- **Tools**: Tavily (Web Search), BeautifulSoup (Web Scraping)
- **Server**: Uvicorn

## Features
- **Web Search**: Automatically searches the web for relevant context.
- **Web Scraping**: Navigates to the search results to scrape detailed information.
- **Writer Agent**: Synthesizes the scraped data into a comprehensive Markdown report.
- **Critic Agent**: Critiques the generated report to ensure accuracy, completeness, and structure.

---

## Setup & Installation

**Prerequisites:** Python 3.9+

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory and add the following keys:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
   *(Note: Ensure you have access to Mistral and Tavily APIs).*

3. **Run the Server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`.
   You can view the interactive Swagger documentation at `http://localhost:8000/docs`.

---

## API Documentation for Frontend Integration

The Frontend Agent should primarily interact with the following endpoint to generate research reports.

### 1. Run Research Pipeline
**Endpoint:** `POST /api/research`

**Description:** Triggers the AI research pipeline for a specific topic. Be aware that this process can take some time (up to 30-60 seconds) depending on the topic, as it triggers multiple LLM calls and web requests.

**Request Body (JSON):**
```json
{
  "topic": "The future of quantum computing"
}
```

**Response (JSON - `200 OK`):**
```json
{
  "topic": "The future of quantum computing",
  "search_result": "Raw text output from the initial web search...",
  "reader_result": "Raw text output containing the scraped data from URLs...",
  "writer_result": "Markdown formatted comprehensive report containing Introduction, Key Findings, Conclusion, and Sources...",
  "critic_result": "Markdown formatted critique containing the score, strengths, and areas to improve..."
}
```

> **Frontend Implementation Tips:**
> - Display the `writer_result` (the main report) rendered as Markdown to the user.
> - The `critic_result` can be displayed in a collapsible sidebar or secondary tab for users who want to see the AI's self-evaluation.
> - Consider adding a loading state with steps (Searching -> Scraping -> Writing -> Critiquing) since the pipeline prints updates in the backend. 

### 2. Health Check
**Endpoint:** `GET /api/health`

**Description:** Checks if the server is running.

**Response:**
```json
{
  "status": "ok"
}
```

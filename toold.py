from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("Tavily_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for the given query and return the title,url,and snippet of the top 5 results."""
    result = tavily.search(query, max_results=5)
    out = []
    for i in result["results"]:
        out.append(f"Title: {i['title']}\nURL: {i['url']}\nSnippet: {i['content']}\n")

    return "\n".join(out)


print(web_search.invoke("what are the recent news about war ,iran and russia?"))


@tool
def scrap_url(url: str) -> str:
    """Scrap the given url and return the text content of the page."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        print(f"Error occurred while scraping {url}: {e}")
        return "Error occurred while scraping the URL."


print(scrap_url.invoke("https://www.nbcnews.com/world/iran-war"))

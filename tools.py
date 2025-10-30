import os, re, sys

# Ensure UTF-8 stdout/stderr to avoid cp949 decode errors on Windows consoles
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")
try:
  sys.stdout.reconfigure(encoding="utf-8")
  sys.stderr.reconfigure(encoding="utf-8")
except Exception:
  pass

from crewai.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions

@tool
def web_search_tool(query: str):
  """
  Web Search Tool.
  Args:
    query: str
      The query to search the web for.
  Returns
    A list of search results with the website content in Markdown format.
  """
  app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

  response = app.search(
    query=query,
    limit=5,
    scrape_options=ScrapeOptions(
      formats=["markdown"],
    ),
  )

  if not response.success:
    return "Error using tool."

  cleaned_chunks = []

  for result in response.data:
    title = result["title"]
    url = result["url"]
    markdown = result["markdown"]

    cleaned = re.sub(r"\\+|\n+", "", markdown).strip()
    cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

    cleaned_result = {
      "title": title,
      "url": url,
      "markdown": cleaned,
    }

    cleaned_chunks.append(cleaned_result)

  return cleaned_chunks

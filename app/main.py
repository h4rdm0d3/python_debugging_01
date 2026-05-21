from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from .crawler import Crawler

app = FastAPI(title="python_debugging_01", version="1.0.0")


class CrawlRequest(BaseModel):
    urls: list[str]
    mode: str = "batch"


class PageOut(BaseModel):
    url: str
    title: str = ""
    error: Optional[str] = None


class CrawlStats(BaseModel):
    instance_seen: list[str]


class CrawlResponse(BaseModel):
    results: list[PageOut]
    stats: CrawlStats


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True}


@app.post("/crawl")
async def crawl(req: CrawlRequest) -> CrawlResponse:
    crawler = Crawler()
    pages = await crawler.crawl(req.urls, mode=req.mode)
    return CrawlResponse(
        results=[PageOut(url=p.url, title=p.title, error=p.error) for p in pages],
        stats=CrawlStats(**crawler.stats()),
    )

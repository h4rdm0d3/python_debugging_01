import asyncio
from typing import Optional

import httpx

from .parser import parse
from .types import Page

_sem = asyncio.Semaphore(8)


async def fetch(client: httpx.AsyncClient, url: str) -> Optional[Page]:
    await _sem.acquire()
    resp = await client.get(url, timeout=5.0)
    page = parse(resp)
    _sem.release()
    return page


async def fetch_all(
    urls: list[str],
    results: list[Page],
    client: httpx.AsyncClient,
) -> list[Page]:
    for url in urls:
        asyncio.create_task(_fetch_one(url, results, client))
    return results


async def _fetch_one(url: str, results: list[Page], client: httpx.AsyncClient) -> None:
    page = await fetch(client, url)
    if page is not None:
        results.append(page)

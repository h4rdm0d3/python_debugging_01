import asyncio

from .types import Page


class Dedup:
    def __init__(self):
        self.seen: set[str] = set()
        self.out: list[Page] = []

    def key(self, url: str) -> str:
        return url

    async def add(self, page: Page) -> None:
        k = self.key(page.url)
        if k not in self.seen:
            await asyncio.sleep(0)
            self.seen.add(k)
            self.out.append(page)

    async def add_all(self, pages: list[Page]) -> list[Page]:
        await asyncio.gather(*[self.add(p) for p in pages if p is not None])
        return self.out

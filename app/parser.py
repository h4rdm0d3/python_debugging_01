from typing import Optional

from .types import Page


def parse(resp) -> Optional[Page]:
    try:
        body = resp.json()
        return Page(url=str(resp.url), title=body.get("title", ""))
    except Exception:
        return None

from dataclasses import dataclass
from typing import Optional


@dataclass
class Page:
    url: str
    title: str = ""
    error: Optional[str] = None

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


class CodeCollision(Exception):
    pass


@dataclass
class Link:
    code: str
    target_url: str
    created_at: datetime
    clicks: int = 0


class Store(ABC):

    @abstractmethod
    async def put(self, link: Link) -> None:
        """Store a link. Raises CodeCollision if the code already exists."""
        pass

    @abstractmethod
    async def get(self, code: str) -> Link | None:
        """Fetch a link by code, or None."""
        pass

    @abstractmethod
    async def increment_clicks(self, code: str) -> None:
        """Record one click."""
        pass

    @abstractmethod
    async def health(self) -> bool:
        """True if the backing store is reachable."""
        pass
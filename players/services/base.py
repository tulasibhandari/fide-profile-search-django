from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerProfile:
    fide_id: int
    name: str
    federation: str = ""
    birth_year: Optional[int] = None
    title: str = ""
    gender: str = ""
    standard: Optional[int] = None
    rapid: Optional[int] = None
    blitz: Optional[int] = None
    photo_small: str = ""
    photo_medium: str = ""
    photo_credit: str = ""


class ProviderError(Exception):
    pass


class PlayerNotFound(ProviderError):
    pass
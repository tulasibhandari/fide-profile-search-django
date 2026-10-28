import requests
from .base import PlayerProfile, ProviderError, PlayerNotFound


class LichessProvider:
    BASE = "https://lichess.org/api/fide/player"

    def get_player(self, fide_id: int) -> PlayerProfile:
        try:
            r = requests.get(f"{self.BASE}/{fide_id}", timeout=8)
        except requests.RequestException as exc:
            raise ProviderError(f"lichess: {exc}") from exc

        if r.status_code == 404:
            raise PlayerNotFound(f"No FIDE player with id {fide_id}")
        if r.status_code == 429:
            raise ProviderError("lichess: rate limited, try again later")
        if not r.ok:
            raise ProviderError(f"lichess: HTTP {r.status_code}")

        d = r.json()
        photo = d.get("photo") or {}
        return PlayerProfile(
            fide_id=d["id"],
            name=d.get("name", ""),
            federation=d.get("federation") or "",
            birth_year=d.get("year"),
            title=d.get("title") or "",
            gender=d.get("gender") or "",
            standard=d.get("standard"),
            rapid=d.get("rapid"),
            blitz=d.get("blitz"),
            photo_small=photo.get("small", ""),
            photo_medium=photo.get("medium", ""),
            photo_credit=photo.get("credit", ""),
        )
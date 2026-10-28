import python_fide as fide

from .base import PlayerProfile, ProviderError


class PythonFideProvider:
    name = "python-fide"

    def get_player(self, fide_id: int) -> PlayerProfile:
        try:
            # TODO: use the player-details function from the README.
            # I only confirmed get_opponents, get_rating_progress_chart,
            # get_game_stats from the docs, so check the exact name.
            p = fide.get_player(fide_id)
        except Exception as exc:
            raise ProviderError(f"python-fide: {exc}") from exc

        return PlayerProfile(
            fide_id=fide_id,
            name=getattr(p, "name", ""),
            federation=getattr(p, "federation", None),
            source=self.name,
        )
        
    # def get_rating_history(self, fide_id: int) -> list[dict]:
    #     try:
    #         history = self.client.get_rating_progress_chart(FidePlayerID(fide_id=fide_id))
    #     except InvalidFidePlayerError as exc:
    #         raise ProviderError(f"python-fide: unknown player {fide_id}") from exc
    #     except Exception as exc:
    #         raise ProviderError(f"python-fide: {exc}") from exc

    #     return [
    #         {
    #             "month": str(h.month),
    #             "standard": h.standard.rating,
    #             "rapid": h.rapid.rating,
    #             "blitz": h.blitz.rating,
    #         }
    #         for h in history
    #     ]
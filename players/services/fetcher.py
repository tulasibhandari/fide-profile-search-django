from dataclasses import asdict
from django.utils import timezone
from players.models import FidePlayer
from .lichess import LichessProvider
from .base import ProviderError

_lichess = LichessProvider()


def get_or_fetch_player(fide_id: int, force: bool = False) -> FidePlayer:
    obj = FidePlayer.objects.filter(fide_id=fide_id).first()
    if obj and not force and not obj.is_stale():
        return obj

    try:
        profile = _lichess.get_player(fide_id)
    except ProviderError:
        if obj:          # network problem: serve stale data instead of failing
            return obj
        raise            # includes PlayerNotFound

    data = asdict(profile)
    data.pop("fide_id")
    data["fetched_at"] = timezone.now()
    obj, _ = FidePlayer.objects.update_or_create(fide_id=fide_id, defaults=data)
    return obj
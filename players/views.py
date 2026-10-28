# views.py
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Registration
from .services.base import PlayerNotFound, ProviderError
from .services.fetcher import get_or_fetch_player
from .services.pyfide import PythonFideProvider



_pyfide = PythonFideProvider()


def player_detail(request, fide_id: int):
    try:
        p = get_or_fetch_player(fide_id, force=request.GET.get("refresh") == "1")
    except PlayerNotFound:
        return JsonResponse({"error": "player not found"}, status=404)
    except ProviderError as exc:
        return JsonResponse({"error": str(exc)}, status=502)

    return JsonResponse({
        "fide_id": p.fide_id, "name": p.name, "title": p.title,
        "federation": p.federation, "birth_year": p.birth_year,
        "ratings": {"standard": p.standard, "rapid": p.rapid, "blitz": p.blitz},
        "photo": p.photo_medium, "photo_credit": p.photo_credit,
    })


def player_history(request, fide_id: int):
    key = f"fide-history-{fide_id}"
    data = cache.get(key)
    if data is None:
        try:
            data = _pyfide.get_rating_history(fide_id)
        except ProviderError as exc:
            return JsonResponse({"error": str(exc)}, status=502)
        cache.set(key, data, 60 * 60 * 12)
    return JsonResponse({"fide_id": fide_id, "history": data})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            Registration.objects.create(
                player=form.player,                  # server-fetched, not from the browser
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
            )
            return redirect("register_done")
    else:
        form = RegistrationForm()
    return render(request, "players/register.html", {"form": form})


def register_done(request):
    return render(request, "players/register_done.html")
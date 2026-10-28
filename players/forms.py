from django import forms
from .services.base import PlayerNotFound, ProviderError
from .services.fetcher import get_or_fetch_player


def _readonly(label, **kw):
    # disabled=True is the key: Django ignores submitted values for these fields
    return forms.CharField(label=label, required=False, disabled=True, **kw)


class RegistrationForm(forms.Form):
    fide_id = forms.IntegerField(
        label="FIDE ID", min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "e.g. 1503014"}),
    )

    # Auto-filled display fields (never trusted from the browser)
    name = _readonly("Name")
    title = _readonly("Title")
    federation = _readonly("Federation")
    birth_year = _readonly("Birth year")
    standard = _readonly("Standard")
    rapid = _readonly("Rapid")
    blitz = _readonly("Blitz")

    # Fields the user fills in themselves
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Phone", required=False, max_length=30)

    player = None  # set in clean_fide_id

    def clean_fide_id(self):
        fide_id = self.cleaned_data["fide_id"]
        try:
            self.player = get_or_fetch_player(fide_id)
        except PlayerNotFound:
            raise forms.ValidationError("No FIDE player found with this ID.")
        except ProviderError:
            raise forms.ValidationError(
                "Couldn't reach the FIDE data source right now. Please try again."
            )
        return fide_id
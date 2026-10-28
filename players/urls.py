# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("fide/<int:fide_id>/", views.player_detail, name="fide_player"),
    # path("fide/<int:fide_id>/history/", views.player_history, name="fide_history"),
    path("register/", views.register, name="register"),
    path("register/done/", views.register_done, name="register_done"),
]
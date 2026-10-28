from datetime import timedelta
from django.db import models
from django.utils import timezone


class FidePlayer(models.Model):
    fide_id = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=200)
    federation = models.CharField(max_length=3, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    title = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=1, blank=True)
    standard = models.PositiveSmallIntegerField(null=True, blank=True)
    rapid = models.PositiveSmallIntegerField(null=True, blank=True)
    blitz = models.PositiveSmallIntegerField(null=True, blank=True)
    photo_small = models.URLField(max_length=500, blank=True)
    photo_medium = models.URLField(max_length=500, blank=True)
    photo_credit = models.CharField(max_length=200, blank=True)
    fetched_at = models.DateTimeField(default=timezone.now)

    def is_stale(self, hours=24):
        return timezone.now() - self.fetched_at > timedelta(hours=hours)

    def __str__(self):
        return f"{self.title} {self.name} ({self.fide_id})".strip()
    
    
class Registration(models.Model):
    player = models.ForeignKey(FidePlayer, on_delete=models.PROTECT, related_name="registrations")
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} <{self.email}>"    
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    phone = models.CharField("Телефон", max_length=20, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    about = models.TextField("О себе", blank=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль: {self .user .username }"

    @property
    def average_rating(self):
        from matching.models import Rating

        ratings = Rating.objects.filter(rated_user=self.user)
        if not ratings.exists():
            return None
        return round(sum((r.score for r in ratings)) / ratings.count(), 1)

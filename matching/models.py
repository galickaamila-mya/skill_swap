from django.contrib.auth.models import User
from django.db import models
from skills.models import Skill


class MatchOffer(models.Model):
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("accepted", "Принято"),
        ("rejected", "Отклонено"),
        ("cancelled", "Отменено"),
    ]
    target_skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name="incoming_offers",
        verbose_name="Целевой навык",
    )
    offered_skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name="as_offered_in",
        verbose_name="Предлагаемый навык",
    )
    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="match_offers",
        verbose_name="Инициатор",
    )
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Обмен: {self .offered_skill } → {self .target_skill }"


class Deal(models.Model):
    DEAL_STATUS = [
        ("open", "Открыта"),
        ("completed", "Завершена"),
        ("failed", "Сорвана"),
    ]
    match_offer = models.OneToOneField(
        MatchOffer,
        on_delete=models.CASCADE,
        related_name="deal",
        verbose_name="Предложение",
    )
    status = models.CharField(
        "Статус", max_length=20, choices=DEAL_STATUS, default="open"
    )
    closed_at = models.DateTimeField("Закрыта", null=True, blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Сделка #{self .id } ({self .get_status_display ()})"

    @property
    def partner_for(self):
        return None


class Rating(models.Model):
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name="ratings", verbose_name="Сделка"
    )
    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        verbose_name="Оценивший",
    )
    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_ratings",
        verbose_name="Исполнитель",
    )
    score = models.PositiveSmallIntegerField("Оценка", default=5)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ("deal", "rater", "rated_user")

    def __str__(self):
        return f"{self .rated_user .username }: {self .score }/5"

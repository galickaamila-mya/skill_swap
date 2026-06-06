from django.contrib.auth.models import User
from django.db import models


class SkillCategory(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField("Слаг", unique=True)

    class Meta:
        verbose_name = "Категория навыка"
        verbose_name_plural = "Категории навыков"

    def __str__(self):
        return self.name


class Skill(models.Model):
    SKILL_TYPE_CHOICES = [("offer", "Предлагаю"), ("want", "Хочу изучить")]
    LEVEL_CHOICES = [
        ("beginner", "Начальный"),
        ("intermediate", "Средний"),
        ("advanced", "Продвинутый"),
    ]
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="skills", verbose_name="Владелец"
    )
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skills",
        verbose_name="Категория",
    )
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    skill_type = models.CharField(
        "Тип", max_length=10, choices=SKILL_TYPE_CHOICES, default="offer"
    )
    level = models.CharField(
        "Уровень", max_length=20, choices=LEVEL_CHOICES, default="intermediate"
    )
    portfolio_image = models.ImageField(
        "Портфолио", upload_to="skills/", blank=True, null=True
    )
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
